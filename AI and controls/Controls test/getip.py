import socket
import time


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually connect, just used to find the outgoing interface IP
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def get_broadcast_ip(local_ip):
    parts = local_ip.split(".")
    parts[-1] = "255"  # Assuming subnet mask 255.255.255.0
    return ".".join(parts)


local_ip = get_local_ip()
broadcast_ip = get_broadcast_ip(local_ip)
# broadcast_ip = "192.168.10.255"
print(broadcast_ip)

DISCOVERY_MESSAGE = "DISCOVER_ARDUINO"
UDP_PORT = 420
LISTENER_PORT = 1420
TIMEOUT = 3  # seconds
MAX_DEVICES = 10


def discover_arduinos():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(TIMEOUT)
    sock.bind(("", LISTENER_PORT))

    sock.sendto(DISCOVERY_MESSAGE.encode(), (broadcast_ip, UDP_PORT))
    print("Searching for Arduinos...")

    found = []

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode().strip()
            ip = addr[0]
            print(f"✅ {message} (at {ip})")
            found.append((message, ip))

            if len(found) >= MAX_DEVICES:
                break

    except socket.timeout:
        print("⏱️ Done listening.")
    finally:
        sock.close()
    return found


if __name__ == "__main__":
    devices = discover_arduinos()
    print(f"\nFound {len(devices)} device(s).")
