import socket
import time
from dotenv import load_dotenv, set_key


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
    parts[-1] = "255"
    return ".".join(parts)


def discover_arduinos():
    local_ip = get_local_ip()
    broadcast_ip = get_broadcast_ip(local_ip)

    DISCOVERY_MESSAGE = "DISCOVER_ARDUINO"
    UDP_PORT = 420
    LISTENER_PORT = 1420
    TIMEOUT = 3
    MAX_DEVICES = 10

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(TIMEOUT)
    sock.bind(("", LISTENER_PORT))

    sock.sendto(DISCOVERY_MESSAGE.encode(), (broadcast_ip, UDP_PORT))

    found = []

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode().strip()
            ip = addr[0]
            print(f"✅ {message} (at {ip})")
            found.append((message, ip))
            match message:
                case "CAR1":
                    set_key("ipdata.env", "IP1", ip)
                case "CAR2":
                    set_key("ipdata.env", "IP2", ip)
                case "CAR3":
                    set_key("ipdata.env", "IP3", ip)
                case "CAR4":
                    set_key("ipdata.env", "AI_IP", ip)

            if len(found) >= MAX_DEVICES:
                break

    except socket.timeout:
        pass
    finally:
        sock.close()
