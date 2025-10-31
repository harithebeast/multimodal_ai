"""
Test script to verify YOLO model label mapping
Upload test images and see what the model predicts
"""
from component_detector import detector
from pathlib import Path
import sys

def test_single_image(image_path):
    """Test detection on a single image"""
    print(f"\n{'='*60}")
    print(f"Testing: {image_path}")
    print(f"{'='*60}")
    
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        return
    
    # Read image
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Run detection
    result = detector.detect_components(image_data, conf_threshold=0.15)
    
    if result.get('error'):
        print(f"❌ Error: {result['error']}")
        return
    
    # Display results
    detections = result.get('detections', [])
    print(f"\n✅ Found {len(detections)} components:")
    print(f"\nClass Mapping Used:")
    for idx, name in detector.class_mapping.items():
        print(f"  Model ID {idx} → {name}")
    
    print(f"\nDetections:")
    for i, det in enumerate(detections, 1):
        print(f"  {i}. {det['class']} - {det['confidence']*100:.1f}% confidence")
        print(f"     Bbox: {det['bbox']}")
    
    # Save annotated image
    if result.get('annotated_image'):
        output_path = Path(image_path).parent / f"{Path(image_path).stem}_detected.jpg"
        with open(output_path, 'wb') as f:
            f.write(result['annotated_image'])
        print(f"\n💾 Saved annotated image: {output_path}")

def test_sample_images():
    """Test on sample images from the dataset"""
    # Look for test images in RepairMate dataset
    test_dir = Path(__file__).parent.parent / "RepairMate" / "Final.v2i.yolov11" / "test" / "images"
    
    if not test_dir.exists():
        print(f"❌ Test directory not found: {test_dir}")
        return
    
    # Get first few test images
    image_files = list(test_dir.glob("*.jpg"))[:3]
    
    if not image_files:
        print(f"❌ No test images found in: {test_dir}")
        return
    
    print(f"\n{'='*60}")
    print(f"Testing with {len(image_files)} sample images from dataset")
    print(f"{'='*60}")
    
    for img_path in image_files:
        test_single_image(str(img_path))

if __name__ == "__main__":
    print("\n🔍 YOLO Label Verification Tool")
    print("================================\n")
    
    print("Current Model Configuration:")
    print(f"  Model loaded: {detector.model is not None}")
    print(f"  Model path: {detector.model_path}")
    print(f"\nDefault class names: {detector.default_class_names}")
    print(f"Current class mapping:")
    for idx, name in detector.class_mapping.items():
        print(f"  {idx}: {name}")
    
    if len(sys.argv) > 1:
        # Test specific image provided as argument
        image_path = sys.argv[1]
        test_single_image(image_path)
    else:
        # Test sample images from dataset
        print("\n💡 Tip: Run with image path to test specific image:")
        print("   python test_labels.py path/to/image.jpg")
        test_sample_images()
    
    print("\n" + "="*60)
    print("🎯 Instructions to Fix Label Mapping:")
    print("="*60)
    print("""
1. Look at the annotated images saved above
2. Identify which components are correctly labeled
3. Update component_detector.py class_mapping dictionary:
   
   Example:
   If model shows "Battery" but it's actually RAM:
   self.class_mapping = {
       0: 'RAM',      # Model ID 0 → actually RAM
       3: 'Battery',  # Model ID 3 → actually Battery
       ...
   }

4. Restart the API server (python api.py)
5. Test again with your images
""")
