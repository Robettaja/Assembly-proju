import pygame
import time

pygame.init
pygame.display.init()
pygame.display.set_mode((1, 1))
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick name: {joystick.get_name()}")
last_left_x = 0
last_left_y = 0
DEADZONE = 0.1

try:
    while True:
        pygame.event.pump()

        left_x = joystick.get_axis(0)
        left_y = joystick.get_axis(1)

        if (abs(left_x - last_left_x) > DEADZONE) or (
            abs(left_y - last_left_y) > DEADZONE
        ):
            print(f"Left Stick Moved: X={left_x:.2f}, Y={left_y:.2f}")
            last_left_x = left_x
            last_left_y = left_y

        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nExiting.")
finally:
    pygame.quit()
