# System Architecture

This document explains the overall system architecture of the Guidino robot, including software components, data flow, and control logic.

## High-Level Architecture

The Guidino robot uses a two-tier architecture:

1. **Perception and Decision** (Raspberry Pi)
   - Camera input processing
   - Computer vision algorithms
   - Decision making
   - High-level control

2. **Actuation and Control** (Arduino)
   - Motor control
   - Low-level hardware interfacing
   - Command execution

## Software Components

### Perception System
- **Camera Interface**: Captures real-time video using Raspberry Pi Camera
- **Lane Detection**: Processes images to identify lanes and determine robot position
- **Stop Sign Recognition**: Uses cascade classifier to detect stop signs
- **Obstacle Detection**: Identifies obstacles in the path
- **Horizontal Line Detection**: Recognizes horizontal lines that indicate special actions

### Control System
- **Decision Logic**: Determines appropriate actions based on perception inputs
- **I2C Communication**: Transmits commands from Raspberry Pi to Arduino
- **Motor Control**: Executes movement commands on DC motors

## Data Flow

1. Image capture from Pi Camera
2. Image processing with OpenCV
3. Feature extraction (lanes, stop signs, obstacles)
4. Decision making based on extracted features
5. Command generation (forward, turn left/right, stop, etc.)
6. Command transmission via I2C
7. Command execution on Arduino
8. Feedback/loop to next frame

## Control Logic

The control logic follows this sequence:

1. Capture frame from camera
2. Apply image preprocessing (resize, blur, color conversion)
3. Detect lanes using edge detection and Hough transform
4. Calculate deviation from lane center
5. Check for special features (stop signs, obstacles)
6. Determine appropriate command based on all inputs
7. Send command to Arduino via I2C
8. Repeat process for next frame

## System Interaction Diagram

```
+---------------+      +---------------+      +---------------+
| Camera Module |----->| Raspberry Pi  |----->|    Arduino    |
+---------------+      +---------------+      +---------------+
                       |               |             |
                       | Image         |             |
                       | Processing    |             |
                       |               |             |
                       | Decision      |             |
                       | Making        |             |
                       |               |             |
                       +---------------+             |
                               |                     |
                               | I2C Commands        | Motor Control
                               v                     v
                       +---------------+      +---------------+
                       | Arduino via   |----->|    Motors     |
                       | I2C           |      +---------------+
                       +---------------+
```

## Machine Learning Components

The stop sign detection uses a pre-trained Haar Cascade Classifier:

1. **Training Data**: Positive samples (with stop signs) and negative samples (without)
2. **Feature Extraction**: Haar-like features for object detection
3. **Classification**: AdaBoost algorithm to select best features
4. **Detection**: Multi-stage classifier to efficiently detect objects

## Performance Considerations

- Frame processing rate: 10-15 FPS
- Decision latency: <100ms
- I2C communication speed: 100kHz
- Motor response time: ~50ms

## Future Improvements

1. Add deep learning-based object detection
2. Implement SLAM for mapping and localization
3. Add sensor fusion with additional sensors (ultrasonic, LiDAR)
4. Implement PID control for smoother navigation