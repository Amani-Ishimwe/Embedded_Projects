import sys
import math
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import re

# ----- CONFIG -----
PORT = 'COM5'   # <- change if needed
BAUD = 115200
WINDOW = 200    # number of samples shown
READ_LINES_PER_FRAME = 5

ser = serial.Serial(PORT, BAUD, timeout=1)

pitch_buf = deque(maxlen=WINDOW)
roll_buf  = deque(maxlen=WINDOW)
yaw_buf   = deque(maxlen=WINDOW)
x_idx     = deque(maxlen=WINDOW)

fig = plt.figure(figsize=(9, 6))

# Top: time-series lines
ax1 = fig.add_subplot(2,1,1)
(line_pitch,) = ax1.plot([], [], label="Pitch (°)")
(line_roll,)  = ax1.plot([], [], label="Roll (°)")
(line_yaw,)   = ax1.plot([], [], label="Yaw (°)")
ax1.set_xlim(0, WINDOW)
ax1.set_ylim(-180, 180)
ax1.set_xlabel("Samples")
ax1.set_ylabel("Angle (°)")
ax1.set_title("MPU6050 Pitch (Y), Roll (X), Yaw (Z)")
ax1.legend(loc="upper right")

# Bottom: 3D orientation cube
ax2 = fig.add_subplot(2,1,2, projection="3d")
ax2.set_xlim([-2, 2])
ax2.set_ylim([-2, 2])
ax2.set_zlim([-2, 2])
ax2.set_title("3D Orientation (Colored Cube)")
ax2.set_box_aspect([1,1,1])

# Cube vertices
cube_definition = np.array([
    [-1, -1, -1],
    [+1, -1, -1],
    [+1, +1, -1],
    [-1, +1, -1],
    [-1, -1, +1],
    [+1, -1, +1],
    [+1, +1, +1],
    [-1, +1, +1]
])

# Cube faces
faces = [
    [0,1,2,3], # bottom
    [4,5,6,7], # top
    [0,1,5,4], # front
    [2,3,7,6], # back
    [1,2,6,5], # right
    [0,3,7,4]  # left
]

face_colors = ["red", "green", "blue", "orange", "yellow", "cyan"]

poly3d = [[cube_definition[vert] for vert in face] for face in faces]
cube_collection = Poly3DCollection(poly3d, facecolors=face_colors, linewidths=1, edgecolors="black", alpha=0.8)
ax2.add_collection3d(cube_collection)

# --- Parsing function ---
num_re = re.compile(r"[-+]?\d*\.\d+|[-+]?\d+")

def parse_line(line):
    found = num_re.findall(line)
    if len(found) >= 3:
        return float(found[0]), float(found[1]), float(found[2])
    return None, None, None

# --- Rotation matrix with yaw ---
def rotation_matrix(pitch, roll, yaw):
    p = math.radians(pitch)
    r = math.radians(roll)
    y = math.radians(yaw)

    Rx = np.array([[1,0,0],
                   [0, math.cos(r), -math.sin(r)],
                   [0, math.sin(r),  math.cos(r)]])
    Ry = np.array([[ math.cos(p),0, math.sin(p)],
                   [0,1,0],
                   [-math.sin(p),0, math.cos(p)]])
    Rz = np.array([[math.cos(y), -math.sin(y),0],
                   [math.sin(y),  math.cos(y),0],
                   [0,0,1]])
    # apply roll(X), pitch(Y), yaw(Z)
    return Rz @ Ry @ Rx

# --- Animation functions ---
def init():
    line_pitch.set_data([], [])
    line_roll.set_data([], [])
    line_yaw.set_data([], [])
    return (line_pitch, line_roll, line_yaw, cube_collection)

def update(frame):
    for _ in range(READ_LINES_PER_FRAME):
        raw = ser.readline().decode(errors='ignore')
        if not raw:
            break
        pitch, roll, yaw = parse_line(raw)
        if pitch is None:
            continue
        pitch_buf.append(pitch)
        roll_buf.append(roll)
        yaw_buf.append(yaw)
        x_idx.append(len(x_idx) + 1 if x_idx else 1)

    # Update time-series
    xs = list(range(len(x_idx)))
    line_pitch.set_data(xs, list(pitch_buf))
    line_roll.set_data(xs, list(roll_buf))
    line_yaw.set_data(xs, list(yaw_buf))
    ax1.set_xlim(max(0, len(xs)-WINDOW), max(WINDOW, len(xs)))

    # Update cube orientation
    if pitch_buf:
        R = rotation_matrix(pitch_buf[-1], roll_buf[-1], yaw_buf[-1])
        rotated = cube_definition @ R.T
        poly3d_rot = [[rotated[vert] for vert in face] for face in faces]
        cube_collection.set_verts(poly3d_rot)

    return (line_pitch, line_roll, line_yaw, cube_collection)

ani = animation.FuncAnimation(fig, update, init_func=init, interval=30, blit=False)
plt.tight_layout()
plt.show()
