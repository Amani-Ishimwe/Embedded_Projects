import sys
import math
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# ----- CONFIG -----
PORT = 'COM5'
BAUD = 115200
WINDOW = 200   # number of samples shown

ser = serial.Serial(PORT, BAUD, timeout=1)

pitch_buf = deque(maxlen=WINDOW)
x_idx = deque(maxlen=WINDOW)

fig, ax = plt.subplots(figsize=(9, 4))

(line_pitch,) = ax.plot([], [], label="Pitch (°)", color='blue')
ax.set_xlim(0, WINDOW)
ax.set_ylim(-90, 90)
ax.set_xlabel("Samples")
ax.set_ylabel("Angle (°)")
ax.set_title("MPU6050 Pitch (Y)")
ax.legend(loc="upper right")

def parse_line(line):
    # expecting only "pitch"
    try:
        pitch = float(line.strip())
        return pitch
    except:
        return None

def init():
    line_pitch.set_data([], [])
    return (line_pitch,)

def update(frame):
    # Read serial data
    for _ in range(5):
        raw = ser.readline().decode(errors='ignore')
        if not raw:
            break
        pitch = parse_line(raw)
        if pitch is None:
            continue
        pitch_buf.append(pitch)
        x_idx.append(len(x_idx) + 1 if x_idx else 1)

    # Update line graph
    xs = list(range(len(x_idx)))
    line_pitch.set_data(xs, list(pitch_buf))
    ax.set_xlim(max(0, len(xs) - WINDOW), max(WINDOW, len(xs)))

    return (line_pitch,)

ani = animation.FuncAnimation(fig, update, init_func=init, interval=30, blit=True)
plt.tight_layout()
plt.show()
