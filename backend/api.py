from contextlib import asynccontextmanager
import os
from uuid import uuid4
import base64

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from livekit.api import LiveKitAPI, ListRoomsRequest, AccessToken, VideoGrants, CreateRoomRequest
from pydantic import BaseModel
import uvicorn

try:
    from livekit.plugins import google
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from component_detector import detector

load_dotenv()

# Get LiveKit API key and secret from environment variables
api_key = os.environ.get('LIVEKIT_API_KEY')
api_secret = os.environ.get('LIVEKIT_API_SECRET')
livekit_url = os.environ.get('LIVEKIT_URL')
gemini_api_key = os.environ.get('GOOGLE_API_KEY')

# Configure Gemini if available
if GEMINI_AVAILABLE and gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    # Use Gemini 2.0 Flash for best quota: 15 RPM, 1M tokens/min, 200 requests/day
    try:
        vision_model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Using Gemini 2.0 Flash (200 requests/day, 1M tokens/min)")
    except Exception as e:
        print(f"⚠️ Failed to load Gemini 2.0 Flash, trying alternatives: {e}")
        try:
            # Fallback to 2.5 Flash (10 RPM, 250 requests/day)
            vision_model = genai.GenerativeModel('gemini-2.5-flash')
            print("✅ Using Gemini 2.5 Flash (250 requests/day)")
        except Exception as e2:
            print(f"⚠️ Gemini model load error: {e2}")
            vision_model = None
else:
    vision_model = None

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, in production specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/get-token")
async def get_token(participant: str):
    if not api_key or not api_secret:
        raise HTTPException(status_code=500, detail="LiveKit API credentials not configured")

    room_name = ""
    async with LiveKitAPI() as client:
        room = await client.room.create_room(
            CreateRoomRequest(
                name=f"test-room-{uuid4().hex}",
                departure_timeout=60,
            ),
        )
        room_name = room.name
    
    token = AccessToken(api_key, api_secret) \
        .with_identity("participant") \
        .with_name(participant) \
        .with_grants(VideoGrants(
            room=room_name,
            room_join=True,
            can_subscribe=True,
            can_publish=True,
        ))
    
    return {
        "token": token.to_jwt(),
        "url": livekit_url
    }

@app.post("/api/detect-component")
async def detect_component(image: UploadFile = File(...)):
    """Analyze uploaded image to detect hardware components using Gemini Vision AI"""
    try:
        # Read image file
        image_data = await image.read()
        
        # Step 1: Gemini Detection with Bounding Boxes
        try:
            gemini_result = detector.detect_components(image_data)
        except Exception as e:
            error_msg = str(e)
            # Check if it's a quota error
            if "quota" in error_msg.lower() or "429" in error_msg:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "API Quota Exceeded",
                        "message": "You've reached the daily limit for Gemini API requests. Please wait or upgrade your API plan.",
                        "details": "Free tier: 50 requests/day. Consider using gemini-1.5-flash or upgrading.",
                        "retry_after": "Please try again in a few hours or tomorrow."
                    }
                )
            raise
        
        if gemini_result.get("error"):
            error_detail = gemini_result["error"]
            if "quota" in error_detail.lower() or "429" in str(error_detail):
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "API Quota Exceeded",
                        "message": "Daily API limit reached. Please try again later.",
                        "details": error_detail
                    }
                )
            raise HTTPException(status_code=500, detail=error_detail)
        
        detections = gemini_result.get("detections", [])
        annotated_image = gemini_result.get("annotated_image")
        
        # Generate description
        detection_description = detector.generate_description(detections)
        
        # Step 2: Detailed Gemini Analysis (optional, skip if quota issue)
        detailed_analysis = ""
        if GEMINI_AVAILABLE and gemini_api_key and vision_model:
            try:
                import PIL.Image
                import io
                pil_image = PIL.Image.open(io.BytesIO(image_data))
                
                # Create enhanced prompt with detections
                detected_components = ", ".join([d['class'] for d in detections]) if detections else "none"
                
                prompt = f"""You are a hardware upgrade expert assistant. 

I detected these components: {detected_components}

Now provide detailed information:
1. Confirm component identifications
2. Specify exact types/form factors (DDR4/DDR5, M.2 2280, SO-DIMM, etc.)
3. Any visible model numbers or brand names
4. Compatibility notes and upgrade recommendations
5. Condition assessment

Keep response clear and helpful."""

                response = vision_model.generate_content([prompt, pil_image])
                detailed_analysis = response.text
            except Exception as e:
                error_msg = str(e)
                print(f"Detailed analysis error: {error_msg}")
                if "quota" in error_msg.lower() or "429" in error_msg:
                    detailed_analysis = "⚠️ Detailed analysis unavailable due to API quota limits. Basic component detection still works!"
                else:
                    detailed_analysis = f"Detailed analysis unavailable: {str(e)}"
        
        # Combine detection + detailed analysis
        combined_analysis = f"🔍 {detection_description}\n\n📋 Detailed Analysis:\n{detailed_analysis}" if detailed_analysis else detection_description
        
        # Generate structured instructions for the agent
        try:
            structured_data = detector.generate_structured_instructions(detections)
        except Exception as e:
            print(f"Structured data generation error: {str(e)}")
            import traceback
            traceback.print_exc()
            structured_data = {
                "summary": "Error generating structured data",
                "components": [],
                "recommendations": []
            }
        
        # Convert annotated image to base64
        annotated_base64 = ""
        if annotated_image:
            annotated_base64 = base64.b64encode(annotated_image).decode('utf-8')
        
        return {
            "analysis": combined_analysis,
            "detections": detections,
            "annotated_image": f"data:image/jpeg;base64,{annotated_base64}" if annotated_base64 else None,
            "total_components": len(detections),
            "component_detected": len(detections) > 0,
            "model_used": "gemini-2.0-flash",  # YOLO temporarily disabled
            "structured_data": structured_data  # NEW: Structured array with recommendations
        }
    
    except Exception as e:
        print(f"API Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image: {str(e)}"
        )

@app.get("/api/model-info")
async def model_info():
    """Get information about the loaded detection model"""
    model_info_data = {
        "yolo_loaded": False,  # YOLO temporarily disabled
        "gemini_loaded": detector.gemini_model is not None if hasattr(detector, 'gemini_model') else False,
    }
    
    model_name = "Gemini 2.0 Flash (YOLO disabled)"
    
    return {
        "model_type": "Gemini Vision Detection",
        "model_name": model_name,
        "yolo_model": "Temporarily disabled (commented out)",
        "gemini_model": "gemini-2.0-flash" if model_info_data["gemini_loaded"] else "Not loaded",
        "models_loaded": model_info_data,
        "api_key_configured": detector.api_key is not None if hasattr(detector, 'api_key') else False,
        "quota_info": "Gemini 2.0 Flash: 200 requests/day, 15 RPM, 1M tokens/min",
        "capabilities": [
            "Text-based component detection (YOLO disabled)",
            "Component description generation",
            "Detailed component analysis",
            "Multi-component detection"
        ]
    }

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
