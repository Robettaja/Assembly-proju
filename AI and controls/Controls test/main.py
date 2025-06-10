import pygame
import serial
import socket
import struct
import time
from dotenv import load_dotenv
import os


class User:
    def __init__(
        self, joystick: pygame.joystick.JoystickType, name: str, is_player: bool = True
    ):
        load_dotenv("ipdata.env")
        joystick.init()
        print("Connected to controller:", joystick.get_name(), joystick.get_guid())
        self.id = joystick.get_id() if is_player else -1
        self.name = name
        self.speed = 1.0
        if not is_player:
            self.ip = os.getenv("AI_IP")
        else:
            self.ip = os.getenv("IP" + str(self.id + 1))
        self.is_player = is_player
        self.controller = joystick


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setblocking(False)

pygame.init()
clock = pygame.time.Clock()

pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller connected.")
    exit()
users = []

users.append(User(pygame.joystick.Joystick(0), "Pekka Pomo", True))
users.append(User(pygame.joystick.Joystick(0), "PekPom", False))

PORT = 420


def move_towards_target(current, target, speed, dt):
    if current < target:
        current += speed * dt
        if current > target:
            current = target
    elif current > target:
        current -= speed * dt
        if current < target:
            current = target
    return current


currentX = 0.0
currentY = 0.0

try:
    while True:
        dt = clock.tick(60) / 1000.0
        pygame.event.pump()
        for user in users:
            targetX = user.controller.get_axis(2) * user.speed
            targetY = -user.controller.get_axis(1) * user.speed
            currentX = move_towards_target(currentX, targetX, 0.5, dt)
            currentY = move_towards_target(currentY, targetX, 0.5, dt)
            if user.ip != "0.0.0.0":
                data = struct.pack("ff", currentY, currentX)
                if data:
                    sock.sendto(data, (user.ip, PORT))
        clock.tick(60)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    pygame.quit()
