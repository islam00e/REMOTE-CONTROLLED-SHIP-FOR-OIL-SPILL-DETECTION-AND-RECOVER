#include <SoftwareSerial.h>

SoftwareSerial bluetooth(10, 11); // RX, TX pins

const int relay1_forward = 9; // Motor 1 pin 1
const int relay1_backward = 8; // Motor 1 pin 2
const int relay2_forward = 7; // Motor 2 pin 1
const int relay2_backward = 6; // Motor 2 pin 2

void setup() {
  bluetooth.begin(9600); // Set the Bluetooth communication baud rate
  serial.begian(9600);
  pinMode(relay1_forward, OUTPUT); // Set motor 1 pins as outputs
  pinMode(relay1_backward, OUTPUT);
  pinMode(relay2_forward, OUTPUT); // Set motor 2 pins as outputs
  pinMode(relay2_backward, OUTPUT);
}

void loop() {
  if (bluetooth.available()) { // Check if data is available from Bluetooth
    char command = bluetooth.read(); // Read the incoming byte

    switch (command) {
      case 'F': // Forward command
        forward();
        break;
      case 'B': // Backward command
        backward();
        break;
      case 'L': // Left turn command
        left();
        break;
      case 'R': // Right turn command
        right();
        break;
      case 'S': // Stop command
        stop();
        break;
    }
  }
}

void forward() {
  digitalWrite(relay1_forward, HIGH); // Set motor 1 to forward
  digitalWrite(relay1_backward, LOW);

  digitalWrite(relay2_forward, HIGH); // Set motor 2 to forward
  digitalWrite(relay2_backward, LOW);
}

void backward() {
  digitalWrite(relay1_forward, LOW); // Set motor 1 to backward
  digitalWrite(relay1_backward, HIGH);

  digitalWrite(relay2_forward, LOW); // Set motor 2 to backward
  digitalWrite(relay2_backward, HIGH);
}

void left() {
  digitalWrite(relay1_forward, LOW); // Set motor 1 to stop
  digitalWrite(relay1_backward, LOW);

  digitalWrite(relay2_forward, HIGH); // Set motor 2 to forward
  digitalWrite(relay2_backward, LOW);
}

void right() {
  digitalWrite(relay1_forward, HIGH); // Set motor 1 to forward
  digitalWrite(relay1_backward, LOW);

  digitalWrite(relay2_forward, LOW); // Set motor 2 to stop
  digitalWrite(relay2_backward, LOW);
}

void stop() {
  digitalWrite(relay1_forward, LOW); // Set both motors to stop
  digitalWrite(relay1_backward, LOW);

  digitalWrite(relay2_forward, LOW);
  digitalWrite(relay2_backward, LOW);
}