int sensorPin = A0;
const int relayPin = 8; // Digital pin for relay
float thresholdForWater = 2.5; // Adjust based on sensor calibration

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
}

void loop() {
  controlValveBasedOnSensor();
}

void controlValveBasedOnSensor() {
  float volt = 0;
  for (int i = 0; i < 800; i++) {
    volt += ((float)analogRead(sensorPin) / 1023) * 5;
  }
  volt = volt / 800;

  if (volt < thresholdForWater) { // If water detected
    digitalWrite(relayPin, HIGH);  // Open the valve
    Serial.println("Valve opened (water detected)");
  } else { // If not water (assuming oil)
    digitalWrite(relayPin, LOW);   // Close the valve
    Serial.println("Valve closed (oil detected)");
  }

  delay(100); // Adjust delay as needed
}
