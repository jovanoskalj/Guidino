# Machine Learning Components

This document details the machine learning approaches used in the Guidino robot for computer vision tasks.

## Stop Sign Detection

The stop sign detection in Guidino uses a Haar Cascade Classifier, which is a machine learning-based approach for object detection.

### How Haar Cascade Classifiers Work

Haar Cascade is a machine learning object detection algorithm used to identify objects in an image or video. It is based on the concept of features rather than pixels, making it efficient for real-time applications.

1. **Features**: Haar features are similar to convolutional kernels which are used to detect the presence of specific features in the image.

2. **Training Process**:
   - A classifier is trained with hundreds of positive samples (images with stop signs)
   - And thousands of negative samples (images without stop signs)
   - AdaBoost algorithm is used to select the best features and create a strong classifier

3. **Cascade Structure**:
   - The classifier has multiple stages arranged in a cascade
   - Early stages reject most non-stop-sign regions quickly
   - Later stages perform more detailed analysis on potential stop sign regions

### Training Data

For the stop sign classifier:
- **Positive Samples**: The `stop sign ph/positive/` directory contains images of stop signs
- **Negative Samples**: The `stop sign ph/negative/` directory contains images without stop signs

### Training Process Used

```bash
# Step 1: Create a description file of positive samples
opencv_createsamples -info positive_samples.txt -w 24 -h 24 -vec samples.vec -num 1000

# Step 2: Train the classifier
opencv_traincascade -data cascade/ -vec samples.vec -bg negative_samples.txt \
                   -numPos 900 -numNeg 1800 -numStages 10 -w 24 -h 24
```

The resulting classifier is stored in the `Stop_cascade.xml` file.

### Implementation in Code

The trained classifier is used in the Python code as follows:

```python
# Load the classifier
stop_cascade = cv2.CascadeClassifier('Stop_cascade.xml')

# Use the classifier on each frame
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
stops = stop_cascade.detectMultiScale(gray, 1.3, 5)

# Process detected stop signs
for (x,y,w,h) in stops:
    # Take action when stop sign is detected
    # ...
```

## Lane Detection Approach

Lane detection uses traditional computer vision techniques rather than deep learning:

1. **Image Preprocessing**:
   - Convert to grayscale
   - Apply Gaussian blur
   - Use Canny edge detection

2. **Region of Interest Selection**:
   - Focus on the lower portion of the image where lanes are expected

3. **Hough Line Transform**:
   - Detect line segments in the edge image
   - Group and average to find lane lines

4. **Lane Position Calculation**:
   - Determine the robot's position relative to lane center
   - Calculate steering adjustments needed

### Potential ML-Based Improvements

Future versions could incorporate:

1. **Semantic Segmentation**:
   - Using U-Net or DeepLabV3+ for pixel-wise classification
   - Better lane detection in varying lighting and road conditions

2. **End-to-End Learning**:
   - Training a CNN to directly map from raw images to steering commands
   - Eliminating the need for separate detection and decision steps

## Object Detection

The obstacle detection currently uses contour detection and color thresholding, but could be upgraded to:

1. **YOLO (You Only Look Once)**:
   - Real-time object detection for multiple object classes
   - Implementation on optimized platforms like OpenVINO or TensorRT

2. **MobileNet-SSD**:
   - Lightweight deep learning model suitable for embedded systems
   - Good balance of accuracy and performance on Raspberry Pi

## Performance Optimization

Techniques used to optimize ML performance on the Raspberry Pi:

1. **Model Quantization**:
   - Reducing precision of model weights (32-bit to 8-bit)

2. **Frame Resizing**:
   - Processing smaller images for faster inference

3. **Region of Interest Processing**:
   - Only analyzing relevant portions of the frame

4. **Frame Rate Adjustment**:
   - Balancing between processing speed and control responsiveness