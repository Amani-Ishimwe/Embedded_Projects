import serial, serial.tools.list_ports
import time, math, pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from collections import deque

BAUD_RATE = 38400

def locate_bluetooth_port():
    """Find a Bluetooth COM port automatically"""
    print("🔍 Searching for available serial ports...")
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(f"Port found: {p.device} - {p.description}")
    for p in ports:
        if "Bluetooth" in p.description or "HC" in p.description or "Arduino" in p.description:
            try:
                s = serial.Serial(p.device, BAUD_RATE, timeout=0.2)
                time.sleep(0.3)
                s.flushInput()
                print(f"✅ Connected on {p.device}")
                return s
            except:
                continue
    print("❌ No Bluetooth joystick detected.")
    return None

def decode_joystick(data):
    """Convert X,Y string data to normalized values"""
    try:
        parts = data.strip().replace("DATA,", "").split(",")
        if len(parts) != 2:
            return None, None
        x_val = int(parts[0])
        y_val = int(parts[1])
        x = (x_val - 512) / 512.0
        y = (y_val - 512) / 512.0
        return x, y
    except:
        return None, None

def draw_axes():
    glBegin(GL_LINES)
    glColor3f(1, 0, 0); glVertex3f(-10, 0, 0); glVertex3f(10, 0, 0)
    glColor3f(0, 1, 0); glVertex3f(0, -10, 0); glVertex3f(0, 10, 0)
    glColor3f(0, 0, 1); glVertex3f(0, 0, -10); glVertex3f(0, 0, 10)
    glEnd()

def draw_joystick_plane(x, y, z):
    """Render a simple 3D plane model"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(x * 25, 0, 0, 1)
    glRotatef(-y * 25, 1, 0, 0)

    glBegin(GL_TRIANGLES)
    glColor3f(0.7, 0.7, 0.7)
    glVertex3f(0, 0.2, 0.4)
    glVertex3f(-0.3, -0.2, -0.3)
    glVertex3f(0.3, -0.2, -0.3)
    glEnd()

    glColor3f(0.2, 0.5, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(0.5, 0, 0)
    glVertex3f(-0.5, 0, 0)
    glVertex3f(-0.3, 0, -0.3)
    glVertex3f(0.3, 0, -0.3)
    glEnd()
    
    glPopMatrix()

def start_simulation():
    pygame.init()
    screen = pygame.display.set_mode((1000, 700), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("🛩️ Joystick 3D Controller (Unique Edition)")

    gluPerspective(60, (1000 / 700), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST)

    ser = locate_bluetooth_port()
    if not ser:
        return
    
    plane_x = plane_y = plane_z = 0
    trail = deque(maxlen=150)
    move_speed = 0.15
    colors = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT: running = False
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_axes()

        # Read Bluetooth
        if ser.in_waiting > 0:
            data = ser.readline().decode(errors='ignore').strip()
            x, y = decode_joystick(data)
            if x is not None:
                plane_x += x * move_speed
                plane_y += y * move_speed
                plane_z -= 0.02
                trail.append((plane_x, plane_y, plane_z))

        # Draw trail
        glBegin(GL_LINE_STRIP)
        for i, pos in enumerate(trail):
            c = colors[i % len(colors)]
            glColor3f(*c)
            glVertex3f(*pos)
        glEnd()

        draw_joystick_plane(plane_x, plane_y, plane_z)
        pygame.display.flip()
        time.sleep(0.015)
    
    ser.close()
    pygame.quit()

if __name__ == "__main__":
    start_simulation()
