#include <SoftwareSerial.h>

// RX = 11, TX = 10
SoftwareSerial link(11, 10);

void setup() {
  Serial.begin(38400);
  link.begin(38400);
  Serial.println("🔗 Serial <-> Bluetooth Bridge Started");
}

void loop() {
  // Forward from Serial Monitor → Bluetooth
  while (Serial.available()) {
    char c = Serial.read();
    link.write(c);
  }

  // Forward from Bluetooth → Serial Monitor
  if (link.available()) {
    String msg = link.readStringUntil('\n');
    Serial.print("BT: ");
    Serial.println(msg);
  }
}
