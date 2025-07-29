import asyncio
import threading
import struct
from bleak import BleakClient, BleakScanner
from bleak.backends.winrt.client import BleakClientWinRT
import json
import requests
import time
import pygame

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

frame_lock = threading.Lock()

frame_lock = threading.Lock()
controller_inputs = {}
controller_locks = {}
users = []

PLAYER_DEVICE_MAP = {}


def save_lap_time(username, laps, total_time):
    data = {
        "user": username,
        "laps": laps,
        "total_time": total_time,
    }

    try:
        response = requests.post("http://localhost:8000/api/save-laps", json=data)
        if response.status_code in (200, 201):
            print(
                f"\033[94m[INFO]\033[0mLap time saved to backend for player {username}"
            )
        else:
            print(
                f"\033[91m[ERROR]Failed to save lap time: {response.status_code} {response.text}"
                "\033[0m"
            )
    except requests.exceptions.RequestException as e:
        print(f"\033[91m[ERROR]Request error: {e}\033[0m")



def race_over():
    for user in users:
        if not user.completedRace:
            return False
    return True


class RaceData:
    def __init__(self, laps: int = 1, clockwise: bool = False):
        self.laps = laps  # Kuinka monta kierrosta radalla ajetaan
        self.clockwise = clockwise  # Ajetaan radalla myötäpäivään vai vastapäivään oletus vastapäivään


class User:
    def __init__(
        self,
        car_num: int,
        name: str,  # Pelaajan nimi
        arucoID: int,  # Mitä autoa pelaaja ohjaa (määritetään myöhemmin)
        is_player: bool = True,  # Onko pelaaja vai tekoäly Vain pelaaja 2 kohdalla mahdollinen valita
    ):
        self.car_num = car_num
        self.arucoID = arucoID
        self.raceTime = 0
        self.is_player = is_player
        self.is_on_track = True
        self.completedRace = False
        self.lapTimes = []
        self.nextCheckpointIndex = 0
        self.lapsCompleted = 0
        self.name = name
        self.speed = 1.0
        self.controller_id = 0

        def __hash__(self):
            return hash((self.id, self.name))


def check_controllers():
    pygame.init()
    pygame.joystick.init()
    all_connected = True

    for player in users:
        if pygame.joystick.get_count() <= player.controller_id:
            print(
                f"\033[91m[ERROR] Controller not found for player {player.name} (Controller ID: {player.controller_id})\033[0m"
            )
            all_connected = False

    pygame.quit()
    return all_connected


def py_thread():
    pygame.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()
    joystics = []
    for player in users:
        if pygame.joystick.get_count() <= player.controller_id:
            print("\033[91mController not found for player", player.name, "\033[0m")
        joystick = pygame.joystick.Joystick(player.controller_id)
        joystick.init()
        joystics.append(joystick)
    try:
        while True:
            pygame.event.pump()
            dt = clock.tick(60) / 1000
            for player in users:
                joystick = joystics[player.controller_id]
                if player.checkpointIndex != 0:
                    if player.completedRace:
                        continue
                    if player.is_on_track:
                        player.raceTime += dt
                        player.speed = 1
                    else:
                        joystick.rumble(1, 1, 4)  # Reset rumble
                        player.raceTime += dt * 2
                        player.speed = 0.5

                x = joystick.get_axis(0) * player.speed
                y = -joystick.get_axis(3) * player.speed
                with controller_locks[0]:
                    controller_inputs[0] = (x, y)
            if race_over():
                break

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pygame.quit()


CHAR_UUID = "abcdefab-cdef-1234-5678-abcdefabcdef"
DEVICES = []


async def handle_device(device, player_number):
    async with BleakClient(device.address) as client:
        print(f"\033[94m[INFO]\033[0m [{device.name}] Connected to BLE")

        await asyncio.sleep(0.1)  # let connection stabilize

        while True:
            try:
                with controller_locks[0]:
                    x, y = controller_inputs.get(0, (0.0, 0.0))

                payload = struct.pack("ff", x, y)
                await client.write_gatt_char(CHAR_UUID, payload, response=False)
                await asyncio.sleep(1 / 30)

            except Exception as e:
                await asyncio.sleep(0.05)
            if race_over():
                payload = struct.pack("ff", 0, 0)
                await client.write_gatt_char(CHAR_UUID, payload, response=False)
                return


async def run():
    global x_input, y_input, frame_lock

    print("\033[94m[INFO]\033[0m Scanning for device...")
    devices = await BleakScanner.discover()
    devices = [d for d in devices if d.name in DEVICES]

    if not devices:
        print("\033[91m[ERROR] Device not found.\033[0m")
        return
    tasks = []
    for player_number, device_name in PLAYER_DEVICE_MAP.items():
        device = next((d for d in devices if d.name == device_name), None)
        if device:
            tasks.append(handle_device(device, player_number))
        else:
            print(
                f"\033[91m[P{player_number}] BLE device '{device_name}' not found.\033[0m"
            )
            return

    await asyncio.gather(*tasks)




def start_race():
    from track_vision import race_loop, initialize_data

    users.append(User(2, "Player1", 0))
    race_data = RaceData(laps=1, clockwise=False)

    if not check_controllers():
        print(
            "\033[91m[ABORTING] One or more controllers are missing. Race cannot start.\033[0m"
        )
        return
    for i in range(len(users)):
        controller_locks[i] = threading.Lock()
        DEVICES.append("CAR" + str(users[0].car_num))
        PLAYER_DEVICE_MAP[i + 1] = "CAR" + str(users[0].car_num)
    threading.Thread(target=py_thread, daemon=True).start()
    race_loop(users[0], race_data)

    asyncio.run(run())


if __name__ == "__main__":
    start_race()
