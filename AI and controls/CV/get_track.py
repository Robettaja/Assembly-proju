import requests

# IPs to try (update to match your Pi's actual Wi-Fi IP if needed)
POSSIBLE_IPS = ["192.168.129.140", "192.168.137.2"]


def try_request(ip):
    PORT = 8080
    SAVE_PATH = "Track data/track.jpg"
    try:
        url = f"http://{ip}:{PORT}/snapshot"
        print(f"[INFO] Trying: {url}")
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            with open(SAVE_PATH, "wb") as f:
                f.write(response.content)
            print(f"[SUCCESS] Snapshot saved to {SAVE_PATH} from {ip}")
            return True
        else:
            print(f"[ERROR] HTTP {response.status_code} from {ip}")
    except requests.RequestException as e:
        print(f"[WARN] Failed to reach {ip}: {e}")
    return False


for ip in POSSIBLE_IPS:
    if try_request(ip):
        break
else:
    print("[FAIL] Could not reach the Raspberry Pi on any IP.")
