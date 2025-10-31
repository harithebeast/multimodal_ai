"""
Component Detection Service using YOLO11n from RepairMate + Gemini Vision AI
Provides bounding boxes and detailed component identification
"""
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import re

# Temporarily disable YOLO
# try:
#     from ultralytics import YOLO
#     YOLO_AVAILABLE = True
# except ImportError:
#     YOLO_AVAILABLE = False
#     print("Warning: ultralytics not installed. Install with: pip install ultralytics")
YOLO_AVAILABLE = False  # Disabled for now

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Install with: pip install google-generativeai")

class ComponentDetector:
    def __init__(self):
        self.yolo_model = None
        self.gemini_model = None
        self.api_key = os.environ.get('GOOGLE_API_KEY')
        
        # YOLO model loading temporarily disabled
        # if YOLO_AVAILABLE:
        #     yolo_path = Path(__file__).parent.parent / 'RepairMate' / 'yolo8n.pt'
        #     if yolo_path.exists():
        #         try:
        #             self.yolo_model = YOLO(str(yolo_path))
        #             print(f"✅ Loaded YOLO11n model from RepairMate: {yolo_path}")
        #         except Exception as e:
        #             print(f"❌ Failed to load YOLO model: {e}")
        #     else:
        #         print(f"⚠️ YOLO model not found at: {yolo_path}")
        #         # Try alternative path
        #         alt_path = Path(__file__).parent.parent / 'RepairMate' / 'yolo11n.pt'
        #         if alt_path.exists():
        #             try:
        #                 self.yolo_model = YOLO(str(alt_path))
        #                 print(f"✅ Loaded YOLO11n model from: {alt_path}")
        #             except Exception as e:
        #                 print(f"❌ Failed to load YOLO model from alt path: {e}")
        
        # Load Gemini for detailed analysis
        if GEMINI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            try:
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                print(f"✅ Loaded Gemini 2.0 Flash for detailed analysis")
            except Exception as e:
                print(f"⚠️ Failed to load Gemini: {e}")
    
    def detect_components(self, image_data: bytes, conf_threshold: float = 0.25):
        """
        Analyze hardware components using Gemini Vision AI (YOLO temporarily disabled)
        
        Args:
            image_data: Image file bytes
            conf_threshold: Confidence threshold (not used in Gemini-only mode)
        
        Returns:
            dict with detection results and annotated image
        """
        # Convert bytes to PIL Image
        pil_image = Image.open(io.BytesIO(image_data))
        
        # Use Gemini-only detection (YOLO disabled for now)
        print("🔍 Using Gemini-only detection (YOLO disabled)")
        return self._gemini_only_detection(image_data, pil_image)
        
        # # YOLO detection temporarily disabled
        # detections = []
        # annotated_image_bytes = None
        # 
        # # Convert bytes to images
        # nparr = np.frombuffer(image_data, np.uint8)
        # cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # pil_image = Image.open(io.BytesIO(image_data))
        # 
        # # Step 1: YOLO Detection for bounding boxes
        # if self.yolo_model and YOLO_AVAILABLE:
        #     try:
        #         print("🔍 Running YOLO11n detection...")
        #         results = self.yolo_model(cv_image, conf=conf_threshold)
        #         
        #         # Parse YOLO results
        #         for result in results:
        #             boxes = result.boxes
        #             for box in boxes:
        #                 # Get box coordinates
        #                 x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        #                 confidence = float(box.conf[0])
        #                 class_id = int(box.cls[0])
        #                 
        #                 # Get class name
        #                 class_name = result.names[class_id] if class_id in result.names else f"Class_{class_id}"
        #                 
        #                 detections.append({
        #                     'class': class_name,
        #                     'confidence': confidence,
        #                     'bbox': [int(x1), int(y1), int(x2), int(y2)],
        #                     'type': 'Unknown',
        #                     'position': f"x:{int(x1)}-{int(x2)}, y:{int(y1)}-{int(y2)}",
        #                     'size': f"{int(x2-x1)}x{int(y2-y1)}",
        #                     'details': f"Detected by YOLO with {confidence:.2%} confidence"
        #                 })
        #         
        #         print(f"✅ YOLO detected {len(detections)} components")
        #         
        #         # Draw bounding boxes on image
        #         annotated_image = self._draw_yolo_boxes(pil_image, detections)
        #         
        #     except Exception as e:
        #         print(f"❌ YOLO detection failed: {e}")
        #         # Fallback to Gemini-only detection
        #         return self._gemini_only_detection(image_data, pil_image)
        # else:
        #     print("⚠️ YOLO not available, using Gemini only")
        #     return self._gemini_only_detection(image_data, pil_image)
        # 
        # # Step 2: Use Gemini for detailed component analysis (optional enhancement)
        # if self.gemini_model and GEMINI_AVAILABLE and len(detections) > 0:
        #     try:
        #         component_names = ", ".join([d['class'] for d in detections])
        #         prompt = f"""I detected these components using object detection: {component_names}
        # 
        # For each component, provide:
        # 1. Specific type/form factor (DDR4/DDR5, M.2, SO-DIMM, etc.)
        # 2. Any visible brand names or model numbers
        # 3. Condition assessment
        # 
        # Keep it concise."""
        #         
        #         response = self.gemini_model.generate_content([prompt, pil_image])
        #         # Optionally parse and enhance detections with Gemini details
        #         print("✅ Gemini enhancement complete")
        #     except Exception as e:
        #         print(f"⚠️ Gemini enhancement skipped: {e}")
        # 
        # # Convert annotated image to bytes
        # img_byte_arr = io.BytesIO()
        # annotated_image.save(img_byte_arr, format='JPEG', quality=95)
        # annotated_image_bytes = img_byte_arr.getvalue()
        # 
        # return {
        #     "detections": detections,
        #     "annotated_image": annotated_image_bytes,
        #     "model_used": "yolo11n + gemini-2.0-flash",
    #     "total_components": len(detections)
    # }
    
    # YOLO box drawing method temporarily disabled
    # def _draw_yolo_boxes(self, pil_image, detections):
    #     """Draw bounding boxes on image from YOLO detections"""
    #     draw = ImageDraw.Draw(pil_image)
    #     
    #     # Try to load a font
    #     try:
    #         font = ImageFont.truetype("arial.ttf", 16)
    #     except:
    #         font = ImageFont.load_default()
    #     
    #     # Color map for different components
    #     colors = {
    #         'battery': (255, 152, 0),     # Orange
    #         'ram': (33, 150, 243),         # Blue
    #         'ssd': (76, 175, 80),          # Green
    #         'wifi': (156, 39, 176),        # Purple
    #         'screw': (158, 158, 158),      # Gray
    #         'motherboard': (255, 87, 34),  # Deep Orange
    #         'fan': (0, 188, 212),          # Cyan
    #         'default': (255, 235, 59)      # Yellow
    #     }
    #     
    #     for det in detections:
    #         bbox = det['bbox']
    #         x1, y1, x2, y2 = bbox
    #         class_name = det['class'].lower()
    #         confidence = det['confidence']
    #         
    #         # Get color
    #         color = colors.get(class_name, colors['default'])
    #         
    #         # Draw bounding box
    #         draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
    #         
    #         # Draw label background
    #         label = f"{det['class']} {confidence:.2%}"
    #         bbox_text = draw.textbbox((x1, y1 - 20), label, font=font)
    #         draw.rectangle(bbox_text, fill=color)
    #         
    #         # Draw label text
    #         draw.text((x1, y1 - 20), label, fill=(0, 0, 0), font=font)
    #     
    #     return pil_image
    
    def _gemini_only_detection(self, image_data, pil_image):
        """Fallback to Gemini-only detection when YOLO fails"""
        if not self.gemini_model:
            return {
                "error": "No detection models available",
                "detections": [],
                "annotated_image": None
            }
        
        try:
            prompt = """List all hardware components visible. For each:
COMPONENT: [name]
TYPE: [details]
POSITION: [location]"""
            
            response = self.gemini_model.generate_content([prompt, pil_image])
            detections = self._parse_detailed_response(response.text)
            annotated_image = self._create_visual_annotation(pil_image, detections, response.text)
            
            img_byte_arr = io.BytesIO()
            annotated_image.save(img_byte_arr, format='JPEG', quality=95)
            
            return {
                "detections": detections,
                "annotated_image": img_byte_arr.getvalue(),
                "model_used": "gemini-2.0-flash",
                "total_components": len(detections)
            }
        except Exception as e:
            return {
                "error": str(e),
                "detections": [],
                "annotated_image": None
            }
    
    def _parse_detailed_response(self, response_text: str):
        """Parse Gemini's detailed component descriptions"""
        detections = []
        
        # Split by component blocks
        blocks = response_text.split('---')
        
        for block in blocks:
            if not block.strip():
                continue
            
            try:
                component_info = {}
                
                # Extract component name
                component_match = re.search(r'COMPONENT:\s*([^\n]+)', block, re.IGNORECASE)
                if component_match:
                    component_info['class'] = component_match.group(1).strip()
                else:
                    continue
                
                # Extract type
                type_match = re.search(r'TYPE:\s*([^\n]+)', block, re.IGNORECASE)
                if type_match:
                    component_info['type'] = type_match.group(1).strip()
                else:
                    component_info['type'] = 'Unknown'
                
                # Extract position
                position_match = re.search(r'POSITION:\s*([^\n]+)', block, re.IGNORECASE)
                if position_match:
                    component_info['position'] = position_match.group(1).strip()
                else:
                    component_info['position'] = 'Unknown'
                
                # Extract size
                size_match = re.search(r'SIZE:\s*([^\n]+)', block, re.IGNORECASE)
                if size_match:
                    component_info['size'] = size_match.group(1).strip()
                else:
                    component_info['size'] = 'Medium'
                
                # Extract details
                details_match = re.search(r'DETAILS:\s*([^\n]+)', block, re.IGNORECASE)
                if details_match:
                    component_info['details'] = details_match.group(1).strip()
                else:
                    component_info['details'] = ''
                
                # Assign confidence based on detail level
                component_info['confidence'] = 0.9 if component_info['details'] else 0.7
                
                detections.append(component_info)
            
            except Exception as e:
                print(f"Error parsing block: {e}")
                continue
        
        return detections
    
    def _create_visual_annotation(self, pil_image: Image, detections: list, full_text: str):
        """Create visual annotation with component labels and information overlay"""
        # Create a copy
        img_draw = pil_image.copy()
        draw = ImageDraw.Draw(img_draw, 'RGBA')
        
        # Try to load fonts
        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            label_font = ImageFont.truetype("arial.ttf", 18)
            small_font = ImageFont.truetype("arial.ttf", 14)
        except:
            title_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        width, height = pil_image.size
        
        # Add semi-transparent overlay at bottom for component list
        overlay_height = min(250, int(height * 0.3))
        draw.rectangle(
            [(0, height - overlay_height), (width, height)],
            fill=(0, 0, 0, 200)
        )
        
        # Add title
        title = f"🔍 Detected {len(detections)} Component{'s' if len(detections) != 1 else ''}"
        draw.text((15, height - overlay_height + 10), title, fill='white', font=title_font)
        
        # List components in overlay
        y_offset = height - overlay_height + 45
        for i, det in enumerate(detections[:6]):  # Show max 6 components
            component_text = f"• {det['class']}"
            if det.get('type') and det['type'] != 'Unknown':
                component_text += f" ({det['type']})"
            if det.get('position') and det['position'] != 'Unknown':
                component_text += f" - {det['position']}"
            
            color = self._get_color_for_class(det['class'])
            # Draw colored indicator
            draw.ellipse([(10, y_offset), (20, y_offset + 10)], fill=color)
            draw.text((25, y_offset - 3), component_text, fill='white', font=small_font)
            y_offset += 25
        
        if len(detections) > 6:
            draw.text((25, y_offset - 3), f"... and {len(detections) - 6} more", 
                     fill='gray', font=small_font)
        
        # Add watermark
        watermark = "Analyzed by Gemini Vision AI"
        draw.text((width - 230, 15), watermark, fill=(255, 255, 255, 180), font=small_font)
        
        return img_draw
    
    def _get_color_for_class(self, class_name: str):
        """Get consistent color for each component class"""
        class_lower = class_name.lower()
        
        # Define colors (RGBA with some transparency)
        if 'battery' in class_lower:
            return (255, 165, 0, 255)  # Orange
        elif 'ssd' in class_lower or 'storage' in class_lower or 'drive' in class_lower:
            return (0, 255, 0, 255)    # Green
        elif 'screw' in class_lower:
            return (255, 255, 0, 255)  # Yellow
        elif 'ram' in class_lower or 'memory' in class_lower:
            return (0, 100, 255, 255)    # Blue
        elif 'wifi' in class_lower or 'nic' in class_lower or 'network' in class_lower or 'card' in class_lower:
            return (255, 0, 255, 255)  # Magenta
        elif 'motherboard' in class_lower or 'board' in class_lower:
            return (0, 255, 255, 255)  # Cyan
        elif 'fan' in class_lower or 'cooling' in class_lower or 'cooler' in class_lower:
            return (128, 0, 255, 255)  # Purple
        elif 'cable' in class_lower or 'wire' in class_lower or 'connector' in class_lower:
            return (255, 128, 0, 255)  # Dark orange
        else:
            return (180, 180, 180, 255)  # Light gray default
    
    def generate_description(self, detections):
        """Generate human-readable description of detected components"""
        if not detections:
            return "No hardware components detected in the image."
        
        # Build detailed description
        parts = []
        for det in detections:
            component = det['class']
            if det.get('type') and det['type'] != 'Unknown':
                parts.append(f"{component} ({det['type']})")
            else:
                parts.append(component)
        
        if len(parts) <= 3:
            description = "I identified: " + ", ".join(parts) + "."
        else:
            description = f"I identified {len(parts)} components: " + ", ".join(parts[:3]) + f", and {len(parts)-3} more."
        
        return description
    
    def generate_structured_instructions(self, detections):
        """
        Generate structured instruction data for the agent to use
        Returns clear, organized information about each component
        """
        if not detections:
            return {
                "summary": "No components detected",
                "components": [],
                "recommendations": []
            }
        
        components_data = []
        recommendations = []
        
        for idx, det in enumerate(detections, 1):
            component_name = det['class']
            component_type = det.get('type', 'Unknown')
            position = det.get('position', 'Unknown location')
            size = det.get('size', 'Medium')
            details = det.get('details', '')
            
            # Create structured component info
            component_info = {
                "id": idx,
                "name": component_name,
                "type": component_type,
                "position": position,
                "size": size,
                "details": details,
                "upgrade_category": self._categorize_component(component_name)
            }
            
            components_data.append(component_info)
            
            # Generate specific recommendations
            rec = self._generate_component_recommendation(component_name, component_type, position)
            if rec:
                recommendations.append(rec)
        
        return {
            "summary": f"Detected {len(detections)} hardware component(s)",
            "components": components_data,
            "recommendations": recommendations,
            "total_count": len(detections)
        }
    
    def _categorize_component(self, component_name):
        """Categorize component for knowledge base reference"""
        comp_lower = component_name.lower()
        
        if 'ram' in comp_lower or 'memory' in comp_lower:
            return "RAM_UPGRADE"
        elif 'battery' in comp_lower:
            return "BATTERY_REPLACEMENT"
        elif 'ssd' in comp_lower or 'storage' in comp_lower or 'drive' in comp_lower:
            return "SSD_UPGRADE"
        elif 'wifi' in comp_lower or 'nic' in comp_lower or 'network' in comp_lower:
            return "WIFI_CARD_REPLACEMENT"
        elif 'screw' in comp_lower:
            return "FASTENER"
        else:
            return "OTHER_COMPONENT"
    
    def _generate_component_recommendation(self, component_name, component_type, position):
        """Generate specific recommendations based on component"""
        comp_lower = component_name.lower()
        
        if 'ram' in comp_lower or 'memory' in comp_lower:
            return {
                "component": component_name,
                "action": "upgrade_available",
                "message": f"I can help you upgrade this RAM module. Located at: {position}.",
                "next_steps": [
                    "Identify exact RAM type (DDR3/DDR4/DDR5)",
                    "Check motherboard compatibility",
                    "Follow RAM installation procedure"
                ]
            }
        elif 'battery' in comp_lower:
            return {
                "component": component_name,
                "action": "replacement_available",
                "message": f"I can guide you through battery replacement. Located at: {position}.",
                "next_steps": [
                    "Power off and unplug device",
                    "Disconnect battery cable",
                    "Remove battery carefully",
                    "Install new battery"
                ]
            }
        elif 'ssd' in comp_lower or 'storage' in comp_lower:
            return {
                "component": component_name,
                "action": "upgrade_available",
                "message": f"I can help you upgrade this storage drive. Located at: {position}.",
                "next_steps": [
                    "Identify SSD form factor (M.2/2.5\"/etc)",
                    "Check interface type (SATA/NVMe)",
                    "Follow SSD installation procedure"
                ]
            }
        elif 'wifi' in comp_lower or 'nic' in comp_lower:
            return {
                "component": component_name,
                "action": "upgrade_available",
                "message": f"I can help you upgrade this WiFi card. Located at: {position}.",
                "next_steps": [
                    "Identify card form factor (M.2/Mini PCIe)",
                    "Disconnect antenna cables carefully",
                    "Follow WiFi card replacement procedure"
                ]
            }
        elif 'screw' in comp_lower:
            return {
                "component": component_name,
                "action": "tool_required",
                "message": f"Screw identified at: {position}. Ensure you have the right screwdriver.",
                "next_steps": [
                    "Use appropriate screwdriver size",
                    "Remove screw carefully",
                    "Store screw safely for reassembly"
                ]
            }
        
        return None

# Global detector instance
detector = ComponentDetector()
