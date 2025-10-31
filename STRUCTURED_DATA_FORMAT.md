# Structured Component Detection Data Format

## Overview
The component detection system now returns **structured data** that the agent can use to provide clear, organized upgrade instructions.

## Response Structure

### API Response (`/api/detect-component`)
```json
{
  "analysis": "🔍 Detection description\n\n📋 Detailed Analysis:\n...",
  "detections": [...],
  "annotated_image": "data:image/jpeg;base64,...",
  "total_components": 2,
  "component_detected": true,
  "model_used": "gemini-2.0-flash-exp",
  "structured_data": {
    "summary": "Detected 2 hardware component(s)",
    "components": [...],
    "recommendations": [...],
    "total_count": 2
  }
}
```

## Structured Data Details

### 1. `structured_data.components[]` Array
Each detected component has:

```json
{
  "id": 1,
  "name": "RAM Module",
  "type": "DDR4 SO-DIMM",
  "position": "Upper-left memory slot near CPU",
  "size": "Standard DIMM size",
  "details": "Kingston branded, appears to be 8GB capacity",
  "upgrade_category": "RAM_UPGRADE"
}
```

**Upgrade Categories:**
- `RAM_UPGRADE`
- `BATTERY_REPLACEMENT`
- `SSD_UPGRADE`
- `WIFI_CARD_REPLACEMENT`
- `FASTENER` (screws)
- `OTHER_COMPONENT`

### 2. `structured_data.recommendations[]` Array
Each recommendation provides actionable guidance:

```json
{
  "component": "RAM Module",
  "action": "upgrade_available",
  "message": "I can help you upgrade this RAM module. Located at: Upper-left memory slot near CPU.",
  "next_steps": [
    "Identify exact RAM type (DDR3/DDR4/DDR5)",
    "Check motherboard compatibility",
    "Follow RAM installation procedure"
  ]
}
```

**Action Types:**
- `upgrade_available` - Component can be upgraded
- `replacement_available` - Component needs replacement
- `tool_required` - Tool identification for screws/fasteners

## How the Agent Uses This Data

### 1. **Precise Component Reference**
Instead of: "I see RAM in the image"
Now: "I detected a DDR4 SO-DIMM RAM module (Component #1) in the upper-left memory slot near the CPU"

### 2. **Step-by-Step Guidance**
The agent references `next_steps[]` to provide organized instructions:
```
Based on the detected components:

**Component #1: RAM Module (DDR4 SO-DIMM)**
Location: Upper-left memory slot

Let's upgrade it step by step:
Step 1: Identify exact RAM type (DDR3/DDR4/DDR5)
[waits for confirmation]
Step 2: Check motherboard compatibility
[waits for confirmation]
...
```

### 3. **Multi-Component Management**
When multiple components are detected, the agent can:
- List all components with IDs
- Ask which one to upgrade first
- Track progress through each component's upgrade

### 4. **Category-Based Knowledge Lookup**
The `upgrade_category` field allows the agent to:
- Pull correct procedure from knowledge base (dashboard.md sections)
- Reference appropriate troubleshooting steps (export.md)
- Check compatibility requirements (permissions.md)

## Frontend Display

### Visual Presentation
The frontend shows structured recommendations as:

```
📋 Upgrade Instructions

[Component Name]
Message: I can help you upgrade this component...

Next Steps:
1. First step description
2. Second step description
3. Third step description

📊 Summary: Detected 2 hardware component(s)
```

## Example Workflow

### User uploads image of laptop internals

**Backend Processing:**
1. Gemini Vision analyzes image
2. Detects: RAM module, Battery, 3 screws
3. Generates structured data with 5 component objects
4. Creates recommendations for RAM and Battery
5. Returns annotated image + structured data

**Frontend Display:**
1. Shows annotated image with component overlay
2. Displays 2 recommendation cards (RAM, Battery)
3. Lists next steps for each component

**Agent Interaction:**
User: "I want to upgrade the RAM"
Agent: "Great! I detected a DDR4 SO-DIMM RAM module (Component #1) in slot A1. Let's upgrade it safely. First, have you powered off the laptop completely?"
[User confirms]
Agent: "Perfect. Now, do you see the two metal clips on either side of the RAM module?"
[Continues step-by-step using recommendations.next_steps as guide]

## Benefits

✅ **Organized Data** - Array structure instead of plain text
✅ **Agent Clarity** - Structured recommendations guide conversation
✅ **User Experience** - Clear visual presentation with actionable steps
✅ **Scalability** - Easy to add new component types and actions
✅ **Context Awareness** - Agent knows exactly what was detected and where
