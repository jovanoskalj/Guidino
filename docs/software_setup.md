# Software Installation Guide

This document provides step-by-step instructions for setting up the software environment for the Guidino robot.

## Raspberry Pi Setup

### 1. Operating System Installation

1. Download Raspberry Pi OS (previously Raspbian) from the [official website](https://www.raspberrypi.org/software/)
2. Flash the OS to an SD card using Balena Etcher or similar software
3. Insert the SD card into the Raspberry Pi and power it on
4. Complete the initial setup (set username, password, connect to WiFi, etc.)

### 2. Enable Camera and I2C Interface

```bash
sudo raspi-config
```

- Navigate to "Interface Options"
- Enable the Camera interface
- Enable the I2C interface
- Reboot the Raspberry Pi

### 3. Update the System

```bash
sudo apt update
sudo apt upgrade
```

### 4. Install Required Packages

```bash
# Install system dependencies
sudo apt install -y python3-pip python3-opencv python3-picamera2 python3-smbus i2c-tools git

# Clone the Guidino repository
git clone https://github.com/jovanoskalj/Guidino.git
cd Guidino

# Install Python dependencies
pip3 install -r requirements.txt
```

## Arduino Setup

### 1. Install Arduino IDE

Download and install the Arduino IDE from the [official website](https://www.arduino.cc/en/software) or use:

```bash
sudo apt install arduino
```

### 2. Upload the Arduino Code

1. Connect the Arduino to the Raspberry Pi via USB
2. Open Arduino IDE
3. Load the `arduino/arduino_commands.ino` file
4. Select the correct board and port
5. Click the Upload button

### 3. Verify I2C Communication

```bash
# Check if I2C devices are detected
sudo i2cdetect -y 1
```

You should see your Arduino's address (0x08) in the output.

## Testing the Software Components

### 1. Test Camera

```bash
# For picamera2
python3 -c "from picamera2 import Picamera2; picam = Picamera2(); picam.start_preview()"
```

### 2. Test Lane Detection

```bash
python3 src/lane_detection_with_horizontal_stop.py
```

### 3. Test Stop Sign Detection

```bash
python3 src/stop_sign_feature.py
```

## Running the Main Program

To start the main program that integrates all features:

```bash
python3 src/raspberry_code.py
```

## Troubleshooting

### Camera Issues
- Ensure the camera ribbon is correctly inserted
- Verify camera is enabled in raspi-config
- Check for errors in dmesg

### I2C Communication Issues
- Verify wiring connections
- Check that both devices are powered
- Ensure the correct I2C address is being used

### Motor Control Issues
- Check motor driver connections
- Verify Arduino is receiving commands via I2C
- Test motors directly with a simple Arduino script

### OpenCV Issues
- Reinstall OpenCV if facing import errors
- Ensure the correct version is installed