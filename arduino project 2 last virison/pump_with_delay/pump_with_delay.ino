#include <Arduino.h>
#include <SoftwareSerial.h>

// Constants
#define thresholdForWater 2.5

// SoftwareSerial for Bluetooth communication
SoftwareSerial bluetooth(10, 11); // RX, TX pins connected to Bluetooth TX & RX

// Pin definitions
const int sensorPin = A0;
const int relayPin = 8;             // Digital pin for relay
const int relay1_forward = 4;       // Motor 1 pin 1
const int relay1_backward = 5;      // Motor 1 pin 2
const int relay2_forward = 6;       // Motor 2 pin 1
const int relay2_backward = 7;      // Motor 2 pin 2
const int ledPin = 13;              // Pin number for the LED
const int pump1 = 8;

// Variable to track oil detection status
bool oilDetected = false;

// Function prototypes
void forward();
void backward();
void left();
void right();
void stop();
void pump();
void controlValveBasedOnSensor();

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(relayPin, OUTPUT);

  // DC motor for ship movement
  pinMode(relay1_forward, OUTPUT);  // Set motor 1 pins as outputs
  pinMode(relay1_backward, OUTPUT);
  pinMode(relay2_forward, OUTPUT);  // Set motor 2 pins as outputs
  pinMode(relay2_backward, OUTPUT);

  pinMode(pump1, OUTPUT);

  // Initialize the ship control
  stop(); // Stop the ship initially
  digitalWrite(pump1, HIGH);

  // Bluetooth module setup
  bluetooth.begin(9600);  // Use the baud rate appropriate for your module
}

void loop() {
  // Check if data is available from Python
  if (Serial.available() > 0) {
    // Read the data
    String receivedData = Serial.readStringUntil('\n');

    // Act based on the received data
    if (receivedData.equals("oil detected")) {
      oilDetected = true;
      stop();   // Stop the ship when oil is detected
      pump();
      controlValveBasedOnSensor();
    } 
    if (receivedData.equals("no oil detected")) {
      oilDetected = false;
      digitalWrite(pump1, HIGH);
    }
  }

  // Continue ship control only when oil is not detected
  if (!oilDetected && bluetooth.available()) {
    digitalWrite(pump1, HIGH);

    // Check if data is available from Bluetooth
    char command = bluetooth.read();  // Read the incoming byte
    Serial.println("Received Bluetooth command: " + String(command));

    // Perform actions based on Bluetooth commands
    switch (command) {
      case 'F': forward(); break;        // Forward command
      case 'B': backward(); break;       // Backward command
      case 'L': left(); break;           // Left turn command
      case 'R': right(); break;          // Right turn command
      case 'S': stop(); break;           // Stop command
    }
  }
}

// Motor control functions
void forward() {
  digitalWrite(relay1_forward, HIGH);
  digitalWrite(relay1_backward, LOW);
  digitalWrite(relay2_forward, HIGH);
  digitalWrite(relay2_backward, LOW);
}

void backward() {
  digitalWrite(relay1_forward, LOW);
  digitalWrite(relay1_backward, HIGH);
  digitalWrite(relay2_forward, LOW);
  digitalWrite(relay2_backward, HIGH);
}

void left() {
  digitalWrite(relay1_forward, LOW);
  digitalWrite(relay1_backward, LOW);
  digitalWrite(relay2_forward, HIGH);
  digitalWrite(relay2_backward, LOW);
}

void right() {
  digitalWrite(relay1_forward, HIGH);
  digitalWrite(relay1_backward, LOW);
  digitalWrite(relay2_forward, LOW);
  digitalWrite(relay2_backward, LOW);
}

void stop() {
  digitalWrite(relay1_forward, LOW);
  digitalWrite(relay1_backward, LOW);
  digitalWrite(relay2_forward, LOW);
  digitalWrite(relay2_backward, LOW);
}

// Oil detection and pump control
void pump() {
  // Check for oil
  while (oilDetected) {
    // If oil is detected, turn on the pump
    digitalWrite(pump1, LOW);
    String receivedData = Serial.readStringUntil('\n');
    if (receivedData.equals("no oil detected")) {
      oilDetected = false;
    } 
  }
}

// Control valve based on sensor reading
void controlValveBasedOnSensor() {
  float volt = 0;
  for (int i = 0; i < 800; i++) {
    volt += ((float)analogRead(sensorPin) / 1023) * 5;
  }
  volt = volt / 800;

  if (volt < thresholdForWater) {
    digitalWrite(relayPin, HIGH);  // If water detected, open the valve
    Serial.println("Valve opened (water detected)");
  } else {
    digitalWrite(relayPin, LOW);   // If not water (assuming oil), close the valve
    Serial.println("Valve closed (oil detected)");
  }

  delay(100); // Adjust delay as needed
}
