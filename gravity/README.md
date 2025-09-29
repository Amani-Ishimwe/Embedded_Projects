## Gravity (MPU6050) + Pygame Coin Game

**Overview**
- `gravity.ino`: Arduino sketch that initializes the MPU6050 (GY-521) via I2C and streams raw acceleration values `ax, ay, az` over Serial at 9600 baud every 100 ms.
- `gravity.py`: Python game using Pygame that reads the three acceleration values from Serial and moves a ball to collect coins. Score is displayed on screen.

**Hardware**
- Arduino Uno/Nano (or compatible)
- MPU6050 (GY-521) accelerometer/gyroscope module
- USB cable

**Wiring (Arduino Uno)**
- GY-521 `VCC` → `5V`
- GY-521 `GND` → `GND`
- GY-521 `SDA` → `A4`
- GY-521 `SCL` → `A5`

For other boards, map to the I2C pins accordingly.

**Arduino Sketch Behavior (`gravity.ino`)**
- Uses libraries: `Wire.h`, `MPU6050.h`
- Initializes I2C and MPU6050 in `setup()`
- In `loop()` reads acceleration into `ax, ay, az` and prints as comma-separated integers followed by newline
- Serial: 9600 baud; update interval: ~100 ms

**Python Game Behavior (`gravity.py`)**
- Dependencies: `pygame`, `pyserial`
- Window: 800x600 titled "GY-521 Ball Collecting Coins Game"
- Reads lines like `ax, ay, az` from the configured serial port
- Movement thresholds: if `ax` > 2000 move right; `< -2000` move left; if `ay` > 2000 move up; `< -2000` move down
- Ball radius 25; coin radius 15; speed 5 px/tick; 30 FPS target
- Keeps the ball within screen bounds and increments score on coin collision

**Setup**
1) Install Arduino libraries
- `MPU6050` library and ensure `Wire` is available

2) Upload Arduino sketch
- Open `gravity.ino` in Arduino IDE, select board/port, upload

3) Install Python dependencies
```bash
pip install pygame pyserial
```

4) Choose the correct serial port
- `gravity.py` defaults to `COM4`. Change `ser = serial.Serial("COM4", 9600)` to your port (e.g., `COM3`, `/dev/ttyUSB0`).

5) Run the game
```bash
python gravity.py
```

**Notes and Tuning**
- Adjust thresholds (±2000) or `speed` for responsiveness.
- Close Arduino Serial Monitor before running the Python script.
- Decoding errors are ignored via `errors='ignore'`; persistent issues may indicate wrong port/baud.


