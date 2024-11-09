#include <Arduino.h>

const int pumpPin = 17;  // Replace with the actual pin connected to the pump
const int pumpCapacity = 350;  // Gallons per hour (GPH)

float calculateSuctionTime(float oilArea) {
  // Convert oil area to square feet
  float oilAreaFt2 = oilArea * 10.764;

  // Calculate oil volume in gallons (assuming shallow oil slick)
  float oilVolumeGal = oilAreaFt2 * 0.0328;

  // Calculate suction time in hours
  return oilVolumeGal / pumpCapacity;
}

void activatePump(float suctionTime) {
  Serial.println("Activating pump...");

  // Convert suction time from hours to milliseconds
  long pumpOnTimeMs = suctionTime * 3600 * 1000;

  digitalWrite(pumpPin, HIGH);  // Turn on the pump
  delay(pumpOnTimeMs);          // Keep the pump on for the calculated time
  digitalWrite(pumpPin, LOW);   // Turn off the pump

  Serial.println("Pump deactivated.");
}

// Assuming you have a function that retrieves the oil area from the camera
// Replace with your actual camera integration function
float getOilAreaFromCamera() {
  // ... (Your camera code to get the oil area)
}

void setup() {
  pinMode(pumpPin, OUTPUT);
  Serial.begin(9600);  // Optional for debugging
}

void loop() {
  float oilArea = getOilAreaFromCamera();
  float suctionTime = calculateSuctionTime(oilArea);
  activatePump(suctionTime);
}
