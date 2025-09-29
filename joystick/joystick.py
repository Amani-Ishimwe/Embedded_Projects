import pygame
import serial

pygame.init()

win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Joystick game")

character_size = 50
character_color = (0, 255, 0)  
character_x, character_y = win_width // 2, win_height // 2
character_speed = 10

arduino_port = 'COM3'  
ser = serial.Serial(arduino_port, 9600)

running = True

prev_x, prev_y = character_x, character_y

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        line = ser.readline().decode().strip()
        if line:  
            data = line.split(',')
            if len(data) == 3:
                try:
                    joy_x, joy_y, button_state = map(int, data)
                    print(f"x: {joy_x}, y: {joy_y}, button: {button_state}")

                    new_x = character_x + (joy_x - 512) // 100 * character_speed
                    new_y = character_y + (joy_y - 512) // 100 * character_speed

                    new_x = max(character_size // 2, min(win_width - character_size // 2, new_x))
                    new_y = max(character_size // 2, min(win_height - character_size // 2, new_y))

                    if (new_x, new_y) != (prev_x, prev_y):
                        character_x, character_y = new_x, new_y
                        prev_x, prev_y = new_x, new_y

                    character_color = (0, 0, 255) if button_state == 1 else (255, 0, 0)

                except ValueError:
                    print("Invalid data:", data)
            else:
                print("Unexpected number of values:", data)
    except serial.SerialException:
        print("Serial connection error")
        running = False

    win.fill((255, 255, 255))
    pygame.draw.circle(win, character_color, (character_x, character_y), character_size // 2)
    pygame.display.flip()


ser.close()
pygame.quit()
