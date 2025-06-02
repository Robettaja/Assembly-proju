import pygame
import serial
import socket
import time


UDP_IP = "192.168.33.160"
UDP_PORT = 420


def send_cmd(cmd):
    print(UDP_IP, UDP_PORT, cmd)
    global last_cmd
    if cmd != last_cmd:
        sock.sendto(cmd.encode(), (UDP_IP, UDP_PORT))
        last_cmd = cmd
        print(f"Sent: {cmd}")


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
last_cmd = None

pygame.init()

pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller connected.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Connected to: {joystick.get_name()}")

try:
    while True:
        pygame.event.pump()

        lr = joystick.get_axis(0)
        lu = -1 * joystick.get_axis(1)
        data = None
        if lr > 0.9:
            data = "R"
        elif lr < -0.9:
            data = "L"
        if data:
            print("sent data")
            send_cmd(data)
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    joystick.quit()
    pygame.quit()
