import asyncio
import threading
import time
import struct
from bleak import BleakClient, BleakScanner
from bleak.backends.winrt.client import BleakClientWinRT

import pygame

frame_lock = threading.Lock()
controller_inputs = {}
controller_locks = {}
users = []

PLAYER_DEVICE_MAP = {}


class User:
    def __init__(
        self,
        player_number: int,  # Esim pelaaja 1 2
        name: str,  # Pelaajan nimi
        arucoID: int,  # Mitä autoa pelaaja ohjaa (määritetään myöhemmin)
        is_player: bool = True,  # Onko pelaaja vai tekoäly Vain pelaaja 2 kohdalla mahdollinen valita
    ):
        self.player_number = player_number
        self.arucoID = arucoID
        self.raceTime = 0
        self.is_player = is_player
        self.completedRace = False
        self.nextCheckpointIndex = 0
        self.lapsCompleted = 0
        self.name = name
        self.speed = 1.0
        self.is_player = is_player
        self.controller_id = player_number - 1

        def __hash__(self):
            return hash((self.id, self.name))


def py_thread():
    pygame.init()
    pygame.joystick.init()
    joystics = []
    for player in users:
        if pygame.joystick.get_count() <= player.controller_id:
            print("\033[91mJoystick not found for player", player.name, "\033[0m")
            return
        joystick = pygame.joystick.Joystick(player.controller_id)
        joystick.init()
        joystics.append(joystick)
    try:
        while True:
            for player in users:
                pygame.event.pump()
                joystick = joystics[player.controller_id]
                x = joystick.get_axis(0)
                y = -joystick.get_axis(3)
                with controller_locks[player.player_number]:
                    controller_inputs[player.player_number] = (x, y)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pygame.quit()


CHAR_UUID = "2A56"
DEVICES = []


async def handle_device(device, player_number):
    async with BleakClient(device.address) as client:
        print(f"[{device.name}] Connected to BLE")

        await asyncio.sleep(0.1)  # let connection stabilize

        while True:
            try:
                with controller_locks[player_number]:
                    x, y = controller_inputs.get(player_number, (0.0, 0.0))

                payload = struct.pack("ff", x, y)
                await client.write_gatt_char(CHAR_UUID, payload, response=False)
                await asyncio.sleep(1 / 100)

            except Exception as e:
                print(f"[{device.name}] Error: {e}")
                await asyncio.sleep(0.05)


async def run():
    global x_input, y_input, frame_lock

    print("Scanning for device...")
    devices = await BleakScanner.discover()
    devices = [d for d in devices if d.name in DEVICES]

    if not devices:
        print("Device not found.")
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
    users.append(User(1, "Player1", 1))
    users.append(User(2, "Player2", 2))
    for i in range(len(users)):
        controller_locks[i + 1] = threading.Lock()
        DEVICES.append("CAR" + str(users[i].arucoID))
        PLAYER_DEVICE_MAP[i + 1] = "CAR" + str(users[i].arucoID)
    threading.Thread(target=py_thread, daemon=True).start()

    asyncio.run(run())


if __name__ == "__main__":
    start_race()
