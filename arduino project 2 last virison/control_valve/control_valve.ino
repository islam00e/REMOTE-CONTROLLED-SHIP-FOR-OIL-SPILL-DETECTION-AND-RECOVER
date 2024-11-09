int sensorPin = A0;
int valvePin = 12;  // Assuming the valve control pin is connected to digital pin 12
bool valveState = false;  // Variable to track the valve state

void setup() {
  Serial.begin(9600);
  pinMode(valvePin, OUTPUT);  // Set the valve control pin as output
}

void loop() {
  valveState = controlValve();  // Call the function to control the valve based on sensor readings

  // Use valveState for further actions or checks within the loop

  delay(10);
}

bool controlValve() {
  float volt = 0;
  float ntu;

  for (int i = 0; i < 800; i++) {
    volt += ((float)analogRead(sensorPin) / 1023) * 5;
  }
  volt = volt / 800;
  volt = round_to_dp(volt, 2);

  if (volt < 2.5) {
    ntu = 3000;
  } else {
    ntu = -1120.4 * sq(volt) + 5742.3 * volt - 4353.8;
  }

  Serial.print("volt: ");
  Serial.print(volt);
  Serial.print(' v');

  Serial.print("  Turbidity:");
  Serial.print(ntu);
  Serial.print(" NTU");
  Serial.println();

  // Valve control based on sensor reading
  if (ntu > 1000) {  // Oil detected
    digitalWrite(valvePin, LOW);  // Close the valve
    return false;  // Set valve state to closed and return false
  } else {  // Water detected
    digitalWrite(valvePin, HIGH);  // Open the valve
    return true;  // Set valve state to open and return true
  }
}

float round_to_dp(float in_value, int decimal_place) {
  float multiplier = powf(10.0f, decimal_place);
  in_value = roundf(in_value * multiplier) / multiplier;
  return in_value;
}
