import asyncio
import logging
import time
import io
import os
from datetime import datetime, timezone
from typing import Union, AsyncIterable, Optional, List, TYPE_CHECKING
from uuid import uuid4

from dotenv import load_dotenv
from langfuse import Langfuse

if TYPE_CHECKING:
    from langfuse.client import StatefulClient

from livekit import rtc
from livekit.agents import (
    Agent,
    AgentSession,
    ChatContext,
    ChatMessage,
    JobContext,
    FunctionTool,
    ModelSettings,
    RoomInputOptions,
    RoomOutputOptions,
    WorkerOptions,
    UserStateChangedEvent,
    cli,
    stt,
    llm,
)
from livekit.agents.llm import ImageContent, AudioContent
from livekit.plugins import cartesia, deepgram, silero
from google.genai import types
# Choose LLM plugin dynamically: prefer Google (Gemini) when available,
# otherwise fall back to OpenAI plugin. Importing a missing plugin would
# raise at module import time, so do this in a try/except to keep the
# process usable in environments without the Google plugin installed.
try:
    from livekit.plugins import google as _google_plugin
    llm_plugin = _google_plugin
    PROVIDER_FORMAT = "google"
except Exception:
    try:
        from livekit.plugins import openai as _openai_plugin
        llm_plugin = _openai_plugin
        PROVIDER_FORMAT = "openai"
    except Exception:
        # If neither plugin is available, raise a clear error so the
        # developer can install the required extras.
        raise ImportError(
            "Neither 'livekit-plugins-google' nor 'livekit-plugins-openai' is installed. "
            "Install one of them (for example: pip install 'livekit-agents[google]' or 'livekit-agents[openai]')"
        )

try:
    from livekit.plugins.turn_detector.english import EnglishModel
except Exception:
    EnglishModel = None

from knowledge_manager import KnowledgeManager

logger = logging.getLogger("openai-video-agent")
logger.setLevel(logging.INFO)

load_dotenv()
_langfuse = Langfuse()
knowledge_manager = KnowledgeManager()

# Optional: allow disabling inference runners (useful on Windows when IPC
# pipes/sockets are unstable or you don't need inference features).
if os.getenv("LIVEKIT_DISABLE_INFERENCE", "0") == "1":
    try:
        from livekit.agents import inference_runner as _infr

        _infr._InferenceRunner.registered_runners = {}
        logger.info("LIVEKIT_DISABLE_INFERENCE=1 -> inference runners disabled")
    except Exception as _e:
        logger.warning("Failed to disable inference runners: %s", _e)

INSTRUCTIONS = f"""
You are a helpful hardware upgrade assistant AI who can guide users through laptop and desktop computer hardware upgrades when they share images or their screen.

IMPORTANT: Respond in plain text only. Do not use any markdown formatting including bold, italics, bullet points, numbered lists, or other markdown syntax. Your responses will be read aloud by text-to-speech.

When the user shares an image or screen:
- Identify the hardware components you can see
- Determine if upgrades are possible for RAM, battery, SSD, or WiFi card
- Provide step by step upgrade instructions one at a time
- Wait for user confirmation before moving to the next step
- Use the structured data from component detection to give precise guidance

Focus on:
- RAM upgrades for desktop and laptop computers
- Battery replacements for laptops
- SSD and M.2 storage upgrades
- WiFi card replacements
- Tool requirements and safety precautions
- Compatibility checks and specifications

When structured data is available from the image analysis, reference the specific components detected. For example: I detected RAM in Component 1, it appears to be DDR4 SO-DIMM. Would you like to upgrade it?

Always prioritize safety. Remind users to power off devices, unplug power sources, and use anti-static precautions.

Guide users through procedures one step at a time. Do not rush ahead. Wait for confirmation before proceeding to the next step.

{knowledge_manager.format_knowledge()}
"""

class VideoAgent(Agent):
    def __init__(self, instructions: str, room: rtc.Room, llm=None) -> None:
        # Determine LLM instance to use for this agent. Prefer an explicit
        # llm passed in; otherwise use the plugin selected at module import
        # time (llm_plugin). If no plugin was loaded, leave llm as None so
        # the Agent can still start in degraded mode.
        selected_llm = llm
        provider_format = getattr(self, "provider_format", None)
        if selected_llm is None:
            try:
                selected_llm = llm_plugin.LLM(model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp"))
                provider_format = PROVIDER_FORMAT
            except Exception:
                selected_llm = None
                provider_format = PROVIDER_FORMAT if 'PROVIDER_FORMAT' in globals() else "openai"

        # store provider format on the instance for later use
        self.provider_format = provider_format

        super().__init__(
            instructions=instructions,
            llm=selected_llm,
            stt=deepgram.STT(),
            tts=None,  # Gemini Realtime API has native audio, no separate TTS needed
            vad=silero.VAD.load(),
            turn_detection=(EnglishModel() if (EnglishModel is not None and os.getenv('LIVEKIT_ENABLE_TURN_DETECTOR', '0') == '1') else None),
        )
        self.room = room
        self.session_id = str(uuid4())
        self.current_trace = None
        self.frames: List[rtc.VideoFrame] = []
        self.last_frame_time: float = 0
        self.video_stream: Optional[rtc.VideoStream] = None

    async def close(self) -> None:
        await self.close_video_stream()
        if self.current_trace:
            self.current_trace = None
        try:
            _langfuse.flush()
        except Exception:
            pass

    async def close_video_stream(self) -> None:
        if self.video_stream:
            await self.video_stream.aclose()
            self.video_stream = None

    async def on_enter(self) -> None:
        self.session.generate_reply(instructions="introduce yourself very briefly")
        self.session.on("user_state_changed", self.on_user_state_change)
        self.room.on("track_subscribed", self.on_track_subscribed)

    async def on_exit(self) -> None:
        await self.session.generate_reply(
            instructions="tell the user a friendly goodbye before you exit",
        )
        await self.close()

    def get_current_trace(self) -> "StatefulClient":
        class _NoopSpan:
            def update(self, *args, **kwargs): return None
            def end(self, *args, **kwargs): return None

        class _NoopTrace:
            trace_id = None
            def span(self, *args, **kwargs): return _NoopSpan()
            def generation(self, *args, **kwargs): return _NoopSpan()

        if self.current_trace:
            return self.current_trace

        try:
            if hasattr(_langfuse, "start_span"):
                root = _langfuse.start_span(name="video_agent", metadata={"session_id": self.session_id})

                class _LFTrace:
                    def __init__(self, client, root_span):
                        self._client = client
                        self._root = root_span

                    @property
                    def trace_id(self):
                        return getattr(self._root, "trace_id", None)

                    def span(self, name: str, metadata: dict | None = None):
                        return _langfuse.start_span(name=name, metadata=metadata)

                    def generation(self, name: str, model: str | None = None, input: object | None = None):
                        return _langfuse.start_span(name=name, metadata={"model": model, "input": input})

                self.current_trace = _LFTrace(_langfuse, root)
                return self.current_trace
        except Exception:
            pass

        self.current_trace = _NoopTrace()
        return self.current_trace

    def on_user_state_change(self, event: UserStateChangedEvent) -> None:
        logger.info(f"User state changed: {event.old_state} -> {event.new_state}")

    async def on_user_turn_completed(
        self, turn_ctx: ChatContext, new_message: ChatMessage,
    ) -> None:
        if self.current_trace:
            self.current_trace = None
        self.current_trace = self.get_current_trace()
        logger.info(f"User turn completed {self.current_trace.trace_id}")

    async def stt_node(
        self, audio: AsyncIterable[rtc.AudioFrame], model_settings: ModelSettings
    ) -> Optional[AsyncIterable[stt.SpeechEvent]]:
        span = self.get_current_trace().span(name="stt_node", metadata={"model": "deepgram"})
        try:
            async for event in Agent.default.stt_node(self, audio, model_settings):
                if event.type == stt.SpeechEventType.FINAL_TRANSCRIPT:
                    logger.info(f"Speech recognized: {event.alternatives[0].text[:50]}...")
                yield event
        except Exception as e:
            span.update(level="ERROR")
            logger.error(f"STT error: {e}")
            raise
        finally:
            span.end()

    async def llm_node(
        self,
        chat_ctx: llm.ChatContext,
        tools: List[FunctionTool],
        model_settings: ModelSettings
    ) -> AsyncIterable[llm.ChatChunk]:

        copied_ctx = chat_ctx.copy()
        frames_to_use = self.current_frames()

        if frames_to_use:
            for position, frame in frames_to_use:
                image_content = ImageContent(image=frame, inference_detail="high")
                copied_ctx.add_message(
                    role="user",
                    content=[f"{position.title()} view of user during speech:", image_content]
                )
                logger.info(f"Added {position} frame to chat context")
        else:
            copied_ctx.add_message(
                role="system",
                content="The user is not currently sharing their screen. Let them know they need to share their screen for you to provide visual assistance."
            )
            logger.warning("No captured frames available for this conversation")

        try:
            messages, _ = copied_ctx.to_provider_format(format=getattr(self, "provider_format", PROVIDER_FORMAT if 'PROVIDER_FORMAT' in globals() else "openai"))
        except Exception:
            try:
                # If the selected llm exposes a helper utils.to_chat_ctx, use it
                utils = getattr(self.llm, "utils", None) if getattr(self, "llm", None) is not None else None
                if utils and hasattr(utils, "to_chat_ctx"):
                    messages = utils.to_chat_ctx(copied_ctx, cache_key=self.llm)
                else:
                    messages = None
            except Exception:
                messages = None
        
        generation = self.get_current_trace().generation(
            name="llm_generation",
            model="Gemini 2.0 Flash Live",
            input=messages,
        )
        output = ""
        set_completion_start_time = False
        try:
            async for chunk in Agent.default.llm_node(self, copied_ctx, tools, model_settings):
                if not set_completion_start_time:
                    generation.update(
                        completion_start_time=datetime.now(timezone.utc),
                    )
                    set_completion_start_time = True
                if chunk.delta and chunk.delta.content:
                    output += chunk.delta.content
                yield chunk
        except Exception as e:
            generation.update(level="ERROR")
            logger.error(f"LLM error: {e}")
            raise
        finally:
            # Different langfuse clients/wrappers may expect different
            # signatures for end(). Be permissive: try common kwarg first,
            # then try positional, then call without args.
            try:
                generation.end(output=output)
            except TypeError:
                try:
                    generation.end(output)
                except TypeError:
                    try:
                        generation.end()
                    except Exception:
                        # swallow; we don't want tracing failures to break
                        # the agent flow
                        logger.debug("Failed to end generation trace", exc_info=True)

    async def tts_node(
        self, text: AsyncIterable[str], model_settings: ModelSettings
    ) -> AsyncIterable[rtc.AudioFrame]:
        span = self.get_current_trace().span(name="tts_node", metadata={"model": "cartesia"})
        logger.debug("tts_node: starting TTS node")
        try:
            async for event in Agent.default.tts_node(self, text, model_settings):
                try:
                    size = None
                    if hasattr(event, "data"):
                        size = len(event.data)
                    elif hasattr(event, "payload"):
                        size = len(event.payload)
                except Exception:
                    size = None
                logger.debug("tts_node: yielding audio frame type=%s size=%s", type(event).__name__, size)
                yield event
        except Exception as e:
            span.update(level="ERROR")
            logger.error(f"TTS error: {e}")
            raise
        finally:
            span.end()

    def on_track_subscribed(
        self,
        track: rtc.RemoteTrack,
        publication: rtc.RemoteTrackPublication,
        participant: rtc.RemoteParticipant,
    ) -> None:
        if publication.source != rtc.TrackSource.SOURCE_SCREENSHARE:
            return
        logger.info("Screen share track subscribed")
        asyncio.create_task(self.read_video_stream(rtc.VideoStream(track)))

    async def read_video_stream(self, video_stream: rtc.VideoStream) -> None:
        await self.close_video_stream()
        self.video_stream = video_stream
        logger.info("Starting video frame capture")
        frame_count = 0
        async for event in video_stream:
            current_time = time.time()
            if current_time - self.last_frame_time >= 1.0:
                frame = event.frame
                self.frames.append(frame)
                self.last_frame_time = current_time
                frame_count += 1
                logger.info(f"Captured frame #{frame_count}: {frame.width}x{frame.height}")
        logger.info(f"Video frame capture ended - captured {frame_count} frames")

    def current_frames(self) -> List[rtc.VideoFrame]:
        current_frames = []
        if len(self.frames) > 0:
            current_frames.append(("most recent", self.frames[-1]))
            if len(self.frames) >= 3:
                current_frames.append(("first", self.frames[0]))
                if len(self.frames) >= 5:
                    mid_idx = len(self.frames) // 2
                    current_frames.append(("middle", self.frames[mid_idx]))
        logger.info(f"Adding {len(current_frames)} frames to conversation (from {len(self.frames)} available)")
        self.frames = []
        return list(reversed(current_frames))


async def entrypoint(ctx: JobContext) -> None:
    await ctx.connect()
    logger.info(f"Connected to room: {ctx.room.name}")
    logger.info(f"Local participant: {ctx.room.local_participant.identity}")

    if len(ctx.room.remote_participants) == 0:
        logger.info("No remote participants in room, exiting")
        return

    logger.info(f"Found {len(ctx.room.remote_participants)} remote participants")

    # Use Gemini Realtime API for live voice interaction
    default_llm = None
    try:
        from livekit.plugins import google
        default_llm = google.realtime.RealtimeModel(
            model=os.getenv("GEMINI_MODEL", "gemini-live-2.5-flash-preview"),
            voice="Puck",
            temperature=0.8,
            instructions=INSTRUCTIONS,
        )
    except Exception as e:
        logger.warning(f"Failed to load Gemini Realtime model: {e}")
        # Fallback to Realtime API with same model
        try:
            from livekit.plugins import google
            default_llm = google.realtime.RealtimeModel(
                model="gemini-live-2.5-flash-preview",
                voice="Puck",
                temperature=0.8,
                instructions=INSTRUCTIONS,
            )
        except Exception:
            default_llm = None

    # Create AgentSession with the Realtime LLM
    session = AgentSession(llm=default_llm)

    # Configure agent with same LLM
    agent = VideoAgent(instructions=INSTRUCTIONS, room=ctx.room, llm=default_llm)

    room_input = RoomInputOptions(video_enabled=True, audio_enabled=True)
    room_output = RoomOutputOptions(audio_enabled=True, transcription_enabled=True)

    await session.start(
        agent=agent,
        room=ctx.room,
        room_input_options=room_input,
        room_output_options=room_output,
    )


if __name__ == "__main__":
    opts = WorkerOptions(entrypoint_fnc=entrypoint, initialize_process_timeout=60.0)
    cli.run_app(opts)
