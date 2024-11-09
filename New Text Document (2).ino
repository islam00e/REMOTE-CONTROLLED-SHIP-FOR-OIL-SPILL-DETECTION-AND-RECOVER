#include <Arduino.h>
#include <SoftwareSerial.h>



SoftwareSerial bluetooth(10, 11); // RX, TX pins conectet to bluetooth TX & RX
const int relay1_forward = 4; // Motor 1 pin 1
const int relay1_backward = 5; // Motor 1 pin 2
const int relay2_forward = 6; // Motor 2 pin 1
const int relay2_backward = 7; // Motor 2 pin 2


const int ledPin = 13;  // Pin number for the LED

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  //dc motor for ship movement
 pinMode(relay1_forward, OUTPUT); // Set motor 1 pins as outputs
 pinMode(relay1_backward, OUTPUT);
 pinMode(relay2_forward, OUTPUT); // Set motor 2 pins as outputs
 pinMode(relay2_backward, OUTPUT);

}

void loop() {
  // Check if data is available from Python
  if (Serial.available() > 0) {
    // Read the data
    String receivedData = Serial.readStringUntil('\n');
    
    // Act based on the received data
    if (receivedData.equals("oil detected"))
    {
            digitalWrite(ledPin, LOW);

      
if (bluetooth.available()) { // Check if data is available from Bluetooth
    char command = bluetooth.read(); // Read the incoming byte
   printf("command");
   
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
    
    
    
    
    else if (receivedData.equals("no oil detected")) {
      // No oil detected, turn off the LED with a delay
      digitalWrite(ledPin, HIGH);
      
    } 
      // Break out of the loop when a specific condition is met
  }}     
  // Your other loop code}








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
