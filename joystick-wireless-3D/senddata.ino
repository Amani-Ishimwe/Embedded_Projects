#include <SoftwareSerial.h>

// Define HC-05 Bluetooth pins
const int RX_PIN = 11;  // Arduino TX to HC-05 RX
const int TX_PIN = 10;  // Arduino RX to HC-05 TX

SoftwareSerial bluetooth(RX_PIN, TX_PIN);

// Joystick input pins
const int JOY_X = A0;
const int JOY_Y = A1;

void setup() {
  Serial.begin(38400);
  bluetooth.begin(38400);
  
  Serial.println("🎮 Joystick Bluetooth transmitter initialized!");
}

void loop() {
  // Read analog joystick values
  int rawX = analogRead(JOY_X);
  int rawY = analogRead(JOY_Y);

  // Send to Serial Monitor
  Serial.print("X_axis=");
  Serial.print(rawX);
  Serial.print("\tY_axis=");
  Serial.println(rawY);

  // Format for Bluetooth
  bluetooth.print("DATA,");
  bluetooth.print(rawX);
  bluetooth.print(",");
  bluetooth.println(rawY);

  delay(75); // Slight delay for stable communication
}
