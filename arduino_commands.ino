#include <Wire.h>

// Motor pins
const int EnableL = 5;
const int HighL = 6;       // Left motor
const int LowL = 7;

const int EnableR = 10;
const int HighR = 8;       // Right motor
const int LowR = 9;

int i = 0;  // Counter for maneuvers if you want to use it

void setup() {
  Wire.begin(0x08);          // I2C address, must match the one in Python
  Wire.onReceive(receiveEvent);

  pinMode(EnableL, OUTPUT);
  pinMode(HighL, OUTPUT);
  pinMode(LowL, OUTPUT);

  pinMode(EnableR, OUTPUT);
  pinMode(HighR, OUTPUT);
  pinMode(LowR, OUTPUT);

  stopMotors();
}

void loop() {
  // Nothing in loop, all commands come via I2C
}

// -----------------------------------------
// STOP
void stopMotors() {
  analogWrite(EnableL, 0);
  analogWrite(EnableR, 0);
}

// -----------------------------------------
// Forward
void forward(int speed = 200) {
  digitalWrite(HighL, LOW);
  digitalWrite(LowL, HIGH);

  digitalWrite(HighR, LOW);
  digitalWrite(LowR, HIGH);

  analogWrite(EnableL, speed);
  analogWrite(EnableR, speed);
}

// -----------------------------------------
// Turns
void left(int speed = 200) {
  digitalWrite(HighL, HIGH);
  digitalWrite(LowL, LOW);

  digitalWrite(HighR, LOW);
  digitalWrite(LowR, HIGH);

  analogWrite(EnableL, speed);
  analogWrite(EnableR, speed);
}

void right(int speed = 200) {
  digitalWrite(HighL, LOW);
  digitalWrite(LowL, HIGH);

  digitalWrite(HighR, HIGH);
  digitalWrite(LowR, LOW);

  analogWrite(EnableL, speed);
  analogWrite(EnableR, speed);
}

// -----------------------------------------
// U-Turn (full left turn)
void uTurn() {
  left(200);
  delay(800); // try to adjust time for ~180° turn
  stopMotors();
}

// -----------------------------------------
// Object avoidance maneuver
void Object() {
  Serial.println("Executing Object maneuver...");

  // Stop
  stopMotors();
  delay(500);

  // Turn Left
  left(200);
  delay(600);
  stopMotors();
  delay(200);

  // Forward
  forward(200);
  delay(800);
  stopMotors();
  delay(200);

  // Turn Right
  right(200);
  delay(600);
  stopMotors();
  delay(200);

  // Forward again
  forward(150);
  delay(800);
  stopMotors();

  Serial.println("Object maneuver finished.");
}

// -----------------------------------------
// I2C receive handler
void receiveEvent(int howMany) {
  if (howMany >= 1) {
    int command = Wire.read();
    Serial.print("Received command: ");
    Serial.println(command);

    switch (command) {
      case 0: forward(200); break;
      case 1: right(150); break;
      case 2: right(200); break;
      case 3: right(250); break;
      case 4: left(150); break;
      case 5: left(200); break;
      case 6: left(250); break;
      case 7: uTurn(); break;
      case 8: stopMotors(); break;
      case 9: Object(); break;
      default: stopMotors(); break;
    }
  }
}
