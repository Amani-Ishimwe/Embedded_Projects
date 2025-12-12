#include <SoftwareSerial.h>

const int buttonPin = 9;
SoftwareSerial bt(10, 11); // RX, TX

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
  bt.begin(9600);
}

void loop() {
  int buttonState = digitalRead(buttonPin);

  if (buttonState == LOW) {
    Serial.println("Button Pressed");
    bt.write('1');
    delay(300); // debounce delay
  }
}