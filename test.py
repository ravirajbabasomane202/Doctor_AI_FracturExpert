import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Load YOLOv9 model
model = YOLO('best.pt')  # Ensure 'best.pt' is in the current directory or provide the full path

# Load an image
image_path = r'C:\Users\SidMane\Downloads\Fracture\0003_0664918633_03_WRI-R1_M011.png'  # Update with your image path
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for matplotlib

# Run inference
results = model(image_rgb)

# Print results
print(results)

# Display results on the image
plt.figure(figsize=(10, 10))
plt.imshow(results[0].plot())  # results[0].plot() returns an image with detections
plt.axis('off')
plt.show()
