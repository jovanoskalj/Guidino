# Guidino - Autonomous Robot with Computer Vision

![Guidino Robot](https://via.placeholder.com/800x400?text=Guidino+Robot)

## Project Overview

Guidino is an autonomous robot that uses computer vision techniques for navigation and decision making. The system is built using a Raspberry Pi for image processing and an Arduino for motor control. The robot can detect lanes, recognize stop signs, avoid obstacles, and make decisions based on visual inputs from its camera.

## Features

- **Lane Detection**: Automatically detects and follows lanes
- **Stop Sign Recognition**: Recognizes stop signs using a trained cascade classifier
- **Obstacle Detection**: Identifies obstacles in its path and takes appropriate action
- **I2C Communication**: Raspberry Pi communicates with Arduino for motor control
- **Multiple Navigation Modes**: Different driving modes based on environmental conditions

## Hardware Components

- Raspberry Pi (with Pi Camera)
- Arduino board
- DC motors with motor driver
- Chassis and wheels
- Power supply (batteries)
- I2C communication interface
- Camera mount

## Software Architecture

The project consists of several Python scripts for the Raspberry Pi and Arduino code:

- **raspberry_code.py**: Main control script for the Raspberry Pi
- **lane_detection_with_horizontal_stop.py**: Lane detection with horizontal line recognition
- **stop_sign_feature.py**: Stop sign detection using cascade classifier
- **obstacle_stop.py**: Obstacle detection and avoidance
- **arduino_commands.ino**: Motor control on the Arduino side
- **captureStop.py**: Utility for capturing stop sign images

## Getting Started

### Prerequisites

- Raspberry Pi with Raspbian OS
- Pi Camera installed and configured
- Arduino IDE
- Python 3.x
- OpenCV library
- Required Python packages (see requirements.txt)

### Hardware Setup

1. Connect the Raspberry Pi Camera
2. Wire the Arduino to the motor driver
3. Connect the motors to the driver
4. Set up I2C communication between Raspberry Pi and Arduino
5. Attach the camera to the robot chassis
6. Connect the power supply

### Software Installation

1. Clone this repository:
```
git clone https://github.com/jovanoskalj/Guidino.git
cd Guidino
```

2. Install required Python packages:
```
pip install -r requirements.txt
```

3. Upload the Arduino code:
   - Open `arduino_commands.ino` in the Arduino IDE
   - Select your board and port
   - Upload the code

### Running the Robot

1. Connect to your Raspberry Pi (via SSH or directly)
2. Navigate to the project directory
3. Run one of the main scripts:
```
python raspberry_code.py
```

## Machine Learning Details

The stop sign detection feature uses a Haar Cascade Classifier trained on a dataset of positive and negative images. The classifier XML files are included in the repository.

### Training Process

The cascade classifier was trained using:
- Positive samples: Images containing stop signs
- Negative samples: Images without stop signs

## Configuration

Adjust parameters in the Python scripts to fine-tune the robot's behavior:
- Lane detection sensitivity
- Turn angles and motor speeds
- Stop sign detection confidence thresholds
- Obstacle avoidance distances

## Troubleshooting

Common issues and solutions:

- **I2C Communication Errors**: Check wiring and addresses
- **Motor Not Responding**: Verify motor driver connections
- **Camera Not Detected**: Ensure camera is properly connected and enabled

## Contributing

Contributions to improve Guidino are welcome. Please feel free to fork the repository, make changes, and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV community for computer vision libraries
- Raspberry Pi and Arduino communities for resources and support