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


last_lr = 0
last_lu = 0

try:
    while True:
        pygame.event.pump()
        for user in users:
            lr = user.controller.get_axis(2) * user.speed
            lu = -user.controller.get_axis(1) * user.speed
            if user.ip != "0.0.0.0":
                is_changed = lr != last_lr or lu != last_lu
                if is_changed:
                    data = struct.pack("ff", lr, lu)
                    if data:
                        sock.sendto(data, (user.ip, PORT))
                        last_lr = lr
                        last_lu = lu
        clock.tick(60)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    pygame.quit()
