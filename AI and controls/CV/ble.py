import asyncio
import time
from bleak import BleakClient, BleakScanner
from bleak.backends.winrt.client import BleakClientWinRT

CHAR_UUID = "2A56"
DEVICE_NAME = "BLE_Test"


async def run():
    print("Scanning for device...")
    devices = await BleakScanner.discover()
    device = next((d for d in devices if d.name == DEVICE_NAME), None)

    if not device:
        print("Device not found.")
        return

    # Use connection parameters for faster communication
    async with BleakClient(device.address) as client:
        print("Connected!")

        # Optional: Request faster connection parameters on Windows
        # This requires the device to support it
        try:
            # Some devices allow connection parameter updates
            await asyncio.sleep(0.1)  # Let connection stabilize
        except:
            pass

        i = 0
        start_time = time.time()
        message_count = 0
        last_report_time = start_time

        while True:
            try:
                # Create payload
                x = i % 256
                y = (i * 2) % 256
                z = (i * 3) % 256
                payload = bytes([x, y, z])

                # Send without response for speed (if supported)
                await client.write_gatt_char(CHAR_UUID, payload, response=False)

                i += 1
                message_count += 1

                # Report stats every 5 seconds
                current_time = time.time()
                if current_time - last_report_time >= 5.0:
                    elapsed = current_time - last_report_time
                    rate = message_count / elapsed
                    print(
                        f"Sent {message_count} messages in {elapsed:.1f}s = {rate:.1f} Hz"
                    )
                    message_count = 0
                    last_report_time = current_time

                # Higher frequency sending
                await asyncio.sleep(1 / 100)  # 100 Hz attempt

            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(run())
