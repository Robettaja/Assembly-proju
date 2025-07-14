import asyncio
import struct
from bleak import BleakClient, BleakScanner

CHAR_UUID = "2A56"  # Same UUID as Arduino
DEVICE_NAME = "BLE_Test"


async def run():
    print("Scanning for device...")
    devices = await BleakScanner.discover()
    device = next((d for d in devices if d.name == DEVICE_NAME), None)

    if not device:
        print("Device not found.")
        return

    async with BleakClient(device.address) as client:
        print("Connected!")

        i = 0
        while True:
            # Example payload: three 8-bit values
            x = i % 256
            y = (i * 2) % 256
            z = (i * 3) % 256
            payload = bytes([x, y, z])

            await client.write_gatt_char(CHAR_UUID, payload)
            # print(f"Sent: {x}, {y}, {z}")

            i += 1
            # await asyncio.sleep(1 / 60)  # ~60 Hz


asyncio.run(run())
