import pygame
import threading
import serial
import socket
import struct
import time
from getip import discover_arduinos
from dotenv import load_dotenv
import os

intersections = [True, True]
frame_lock = threading.Lock()


def set_user_intersection(index, value):
    with frame_lock:
        intersections[index] = value


def move_towards_target(current, target, speed, dt):
    if current > 0 and target < 0 or current < 0 and target > 0:
        speed /= 1.5
    if current < target:
        current += dt / speed
        if current > target:
            current = target
    elif current > target:
        current -= dt / speed
        if current < target:
            current = target
    return current


class RaceData:
    def __init__(self, laps: int = 1, clockwise: bool = False):
        self.laps = laps  # Kuinka monta kierrosta radalla ajetaan
        self.clockwise = clockwise  # Ajetaan radalla myötäpäivään vai vastapäivään oletus vastapäivään


class User:
    def __init__(
        self,
        player_number: int,  # Esim pelaaja 1 2
        name: str,  # Pelaajan nimi
        arucoID: int,  # Mitä autoa pelaaja ohjaa (määritetään myöhemmin)
        is_player: bool = True,  # Onko pelaaja vai tekoäly Vain pelaaja 2 kohdalla mahdollinen valita
    ):
        load_dotenv("ipdata.env")
        self.id = player_number
        self.arucoID = arucoID
        self.raceTime = 0
        self.is_player = is_player
        self.completedRace = False
        self.nextCheckpointIndex = 0
        self.lapsCompleted = 0
        self.name = name
        self.speed = 1.0
        if not is_player:
            self.ip = os.getenv("AI_IP")
        else:
            self.ip = os.getenv("IP" + str(arucoID))
            self.is_player = is_player
            joystick = pygame.joystick.Joystick(player_number - 1)
            joystick.init()

            print("Connected to controller:", joystick.get_name(), joystick.get_guid())
            self.controller = joystick

        def __hash__(self):
            return hash((self.id, self.name))


def input_loop(player1, player2=None):
    discover_arduinos()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)

    clock = pygame.time.Clock()

    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No controller connected.")
        exit()

    users = [player1]

    if player2:
        users.append(player2)

    PORT = 420

    currentX = 0.0
    currentY = 0.0

    try:
        while True:
            dt = clock.tick(60) / 1000.0
            pygame.event.pump()
            for user in users:
                if not user.completedRace:
                    user.raceTime += dt
                else:
                    continue

                if not intersections[user.id]:
                    user.speed -= 0.1 * dt
                    if user.speed < 0.1:
                        user.speed = 0.1
                else:
                    user.speed = 1.0

                targetY = -user.controller.get_axis(1) * user.speed
                targetX = user.controller.get_axis(3) * user.speed
                currentX = move_towards_target(currentX, targetX, 0.01, dt)
                currentY = move_towards_target(currentY, targetY, 0.5, dt)
                print(currentX, currentY)
                if user.ip != "0.0.0.0":
                    data = struct.pack("ff", currentX, currentY)
                    if data:
                        sock.sendto(data, (user.ip, PORT))
            if all(user.completedRace for user in users):
                print(f"{users[0].name} won")
                break
            clock.tick(60)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()

    pygame.quit()
    data = struct.pack("ff", 0, 0)
    for user in users:
        if data:
            sock.sendto(data, (user.ip, PORT))


def start_race():
    from track_vision import race_loop, initialize_data

    pygame.init()
    user1 = User(1, "Pekka Pomo", 1, True)
    race_data = RaceData(3, True)

    # initialize_data()
    # threading.Thread(
    #     target=race_loop, args=(user1, None, race_data), daemon=True
    # ).start()
    input_loop(user1)


if __name__ == "__main__":
    start_race()
