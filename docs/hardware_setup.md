# Hardware Setup Guide

This document provides detailed instructions for setting up the hardware components of the Guidino robot.

## Components List

1. **Raspberry Pi 4** (or compatible model)
2. **Raspberry Pi Camera Module**
3. **Arduino Uno/Nano**
4. **L298N Motor Driver**
5. **DC Motors (2x)**
6. **Robot Chassis**
7. **Wheels (2x drive wheels + 1x caster wheel)**
8. **Jumper Wires**
9. **Power Supply** (Batteries or Power Bank)
10. **Breadboard** (optional for prototyping)

## Wiring Diagram

### Raspberry Pi to Arduino (I2C Connection)
- Raspberry Pi SDA (GPIO 2) → Arduino A4 (SDA)
- Raspberry Pi SCL (GPIO 3) → Arduino A5 (SCL)
- Raspberry Pi GND → Arduino GND

### Arduino to Motor Driver (L298N)
- Arduino Pin 5 → L298N ENA
- Arduino Pin 6 → L298N IN1
- Arduino Pin 7 → L298N IN2
- Arduino Pin 10 → L298N ENB
- Arduino Pin 8 → L298N IN3
- Arduino Pin 9 → L298N IN4
- Arduino GND → L298N GND

### Motor Driver to Motors
- L298N OUT1, OUT2 → Left Motor
- L298N OUT3, OUT4 → Right Motor

### Power Connections
- Battery (+) → L298N +12V
- Battery (-) → L298N GND
- L298N +5V → Arduino Vin (if not powered separately)

## Camera Setup

1. Connect the Raspberry Pi Camera to the CSI port on the Raspberry Pi
2. Mount the camera at the front of the robot chassis
3. Adjust the angle to ensure proper view of the path ahead

## Assembly Instructions

1. Mount the Arduino and Raspberry Pi on the chassis
2. Attach the motor driver board
3. Connect the motors to the chassis and motor driver
4. Mount the camera at the front of the chassis
5. Connect all wiring according to the diagram
6. Secure all components and wiring

## Power Management

The system requires two power sources:
- 5V for Raspberry Pi (via USB power bank or dedicated supply)
- 7-12V for motors (via battery pack)

Ensure proper voltage regulation to avoid damaging components.

## Testing the Hardware

Before running the full software suite, test individual components:

1. Test motor control using simple Arduino sketches
2. Test the camera using Raspberry Pi camera utilities
3. Verify I2C communication between Raspberry Pi and Arduino
4. Check voltage levels throughout the system