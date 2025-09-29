## Joystick + Pygame Character Demo

**Overview**
- `joystic.ino`: Arduino sketch that reads a 2-axis analog joystick and a push-button, then streams `joyX, joyY, buttonState` over Serial at 9600 baud every 100 ms.
- `joystick.py`: Python program using Pygame that reads joystick data over Serial and moves a circle on screen. The circle color changes based on button state.

**Hardware**
- Arduino Uno/Nano (or compatible)
- 2-axis analog joystick with push-button (SW)
- USB cable

**Wiring (Arduino Uno)**
- Joystick `VCC` → `5V`
- Joystick `GND` → `GND`
- Joystick `VRx` → `A0`
- Joystick `VRy` → `A1`
- Joystick `SW`  → `D2`

The sketch configures `D2` as `INPUT_PULLUP`, so the button reads `1` (HIGH) when released and `0` (LOW) when pressed.

**Arduino Sketch Behavior (`joystic.ino`)**
- Pins: `joyXPin = A0`, `joyYPin = A1`, `buttonPin = 2`
- Serial: 9600 baud
- Prints comma-separated values: `joyX, joyY, buttonState` followed by newline every ~100 ms
- Typical centered analog values are near ~512

**Python Program Behavior (`joystick.py`)**
- Dependencies: `pygame`, `pyserial`
- Window: 800x600 titled "Joystick game"
- Reads a line, splits into 3 integers: `joy_x, joy_y, button_state`
- Movement: `(joy - 512) // 100 * character_speed` is added to the current position; clamps within window
- Color: blue when `button_state == 1` (released), red when `button_state != 1` (pressed with internal pull-up)

**Setup**
1) Upload Arduino sketch
- Open `joystic.ino` in Arduino IDE
- Select the correct board and port
- Upload

2) Install Python dependencies
```bash
pip install pygame pyserial
```

3) Choose the correct serial port
- `joystick.py` defaults to `COM3`. Update `arduino_port = 'COM3'` to match your system (e.g., `COM4`, `/dev/ttyUSB0`, `/dev/ttyACM0`).

4) Run the demo
```bash
python joystick.py
```

**Notes and Tuning**
- If motion is too fast/slow, tweak `character_speed` or the divisor `// 100` used to scale the analog delta.
- Because of `INPUT_PULLUP`, pressing the joystick button pulls the line LOW (`0`). The script shows red when pressed.
- Ensure the Arduino serial monitor is closed before running the Python script.


