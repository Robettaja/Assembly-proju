import cv2 as cv
import threading
import subprocess
import requests
import cv2.aruco as aruco
import numpy as np
import queue
from pathlib import Path

line_pos_x = ""
line_pos_y = ""
frame_queue = queue.Queue(maxsize=1)

user = None


class RaceData:
    def __init__(self, laps: int, clockwise: bool):
        self.laps = laps
        self.clockwise = clockwise


def is_intersecting(mask1, mask2):
    return cv.countNonZero(cv.bitwise_and(mask1, mask2)) > 0


def try_request(ip):
    PORT = 8080
    SAVE_PATH = "Track data/track.jpg"
    try:
        url = f"http://{ip}:{PORT}/snapshot"
        print("\033[94m[INFO]\033[0m Trying: {url}")
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            with open(SAVE_PATH, "wb") as f:
                f.write(response.content)
            print(f"[SUCCESS] Snapshot saved to {SAVE_PATH} from {ip}")
            return True
        else:
            print("\033[91m[ERROR]\033[0m HTTP {response.status_code} from {ip}")
    except requests.RequestException as e:
        print("\033[93m[WARN]\033[0m Failed to reach {ip}: {e}")
    return False


def read_frames():
    global user
    rtsp = "rtsp://raspberrypi:8554/cam1"

    cmd = [
        "ffmpeg",
        "-fflags",
        "nobuffer",
        "-flags",
        "low_delay",
        "-strict",
        "experimental",
        "-analyzeduration",
        "0",
        "-probesize",
        "32",
        "-rtsp_transport",
        "tcp",
        "-i",
        rtsp,
        "-fps_mode",
        "passthrough",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-",
    ]
    width = 1280
    height = 640
    frame_size = width * height * 3

    global process

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)
    while True:
        try:
            if user and user.completedRace:
                break
            if process.stdout:
                raw_frame = process.stdout.read(frame_size)
                if len(raw_frame) != frame_size:
                    print("Frame incomplete or stream ended")
                    break

                frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape(
                    (height, width, 3)
                )
                try:
                    frame_queue.put_nowait(frame)
                except queue.Full:
                    try:
                        frame_queue.get_nowait()
                        frame_queue.put_nowait(frame)
                    except queue.Full:
                        pass
        except Exception as e:
            pass


def get_line_orientation(line):
    coord = np.where(line == 255)
    ys, xs = coord[0], coord[1]
    if len(xs) == 0 or len(ys) == 0:
        return None
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    width = x_max - x_min
    height = y_max - y_min
    if width > height:
        return "horizontal"
    else:
        return "vertical"


def white_pixels_side(mask, axis="y"):
    coord = np.where(mask == 255)
    ys, xs = coord[0], coord[1]
    if ys.size == 0:
        return "none"  # no white pixels

    if axis == "y":
        mean_pos = ys.mean()
        midpoint = mask.shape[0] / 2
        return "top" if mean_pos < midpoint else "bottom"

    elif axis == "x":
        mean_pos = xs.mean()
        midpoint = mask.shape[1] / 2
        return "left" if mean_pos < midpoint else "right"

    else:
        raise ValueError("axis parameter must be 'x' or 'y'")


def get_track_mask(image):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)

    red_mask = cv.bitwise_or(mask1, mask2)

    result = image.copy()

    result[red_mask > 0] = [255, 255, 255]

    gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (21, 21), 0)

    inv = cv.bitwise_not(blur)
    ret, thresh = cv.threshold(inv, 95, 255, cv.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    dilated = cv.dilate(thresh, kernel, iterations=2)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
    mask = np.zeros(image.shape, dtype=np.uint8)

    cv.drawContours(
        mask, [sorted_contours[1]], -1, (255, 255, 255), thickness=cv.FILLED
    )
    cv.drawContours(mask, [sorted_contours[2]], -1, (0, 0, 0), thickness=cv.FILLED)
    # cv.imshow("Track Mask", mask)
    return mask


def get_finishline(img):
    img = cv.resize(img, (1280, 640))
    img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    img = cv.GaussianBlur(img, (5, 5), 0)

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv.inRange(img, lower_red1, upper_red1)
    mask2 = cv.inRange(img, lower_red2, upper_red2)
    red_mask = cv.bitwise_or(mask1, mask2)

    contours, _ = cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
    mask = np.zeros(img2.shape, dtype=np.uint8)
    cv.drawContours(
        mask, [sorted_contours[0]], -1, (255, 255, 255), thickness=cv.FILLED
    )
    global line_pos_x
    global line_pos_y
    line_pos_x = white_pixels_side(mask, axis="x")
    line_pos_y = white_pixels_side(mask, axis="y")

    track = cv.imread("Track data/track_mask.jpg", cv.IMREAD_GRAYSCALE)
    ys, xs = np.where(track == 255)

    if len(xs) > 0 and len(ys) > 0:
        x_min, x_max = xs.min(), xs.max()
        y_min, y_max = ys.min(), ys.max()

        w = x_max - x_min + 1
        h = y_max - y_min + 1
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))

        orientation = get_line_orientation(mask)
        match orientation:
            case "horizontal":
                kernel_height = int(0.05 * h)
                kernel_width = int(1920)
                print(kernel_height, kernel_width)
                kernel = cv.getStructuringElement(
                    cv.MORPH_RECT, (kernel_width, kernel_height)
                )
            case "vertical":
                kernel_height = int(1920)
                kernel_width = int(0.05 * w)
                kernel = cv.getStructuringElement(
                    cv.MORPH_RECT, (kernel_width, kernel_height)
                )

        mask = cv.dilate(mask, kernel, iterations=1)

    # cv.imwrite("Track data/finishline_mask.jpg", mask)
    return mask


def save_checkpoints():
    # Load necessary data
    track_mask = cv.imread("Track data/track_mask.jpg", cv.IMREAD_GRAYSCALE)
    finishline_mask = cv.imread("Track data/finishline_mask.jpg", cv.IMREAD_GRAYSCALE)
    checkpoint1 = np.zeros_like(finishline_mask, dtype=np.uint8)
    checkpoint2 = np.zeros_like(finishline_mask, dtype=np.uint8)

    orientation = get_line_orientation(
        finishline_mask
    )  # expects 'horizontal' or 'vertical'

    match orientation:
        case "vertical":
            # line_location = white_pixels_side(finishline_mask, axis="x")
            ys, xs = np.where(finishline_mask == 255)[:2]
            line_left_point = xs.min() if xs.size > 0 else 0

            cys, cxs = np.where(track_mask == 255)[:2]
            track_left_point = cxs.min() if cxs.size > 0 else 0
            track_right_point = cxs.max() if cxs.size > 0 else 0

            shift = 0
            dist = 0
            match line_pos_x:
                case "left":
                    dist = abs(line_left_point - track_left_point)
                    shift = abs(line_left_point - track_right_point) - dist
                case "right":
                    dist = abs(line_left_point - track_right_point)
                    shift = -(abs(line_left_point - track_left_point)) + dist

            M = np.array([[1.0, 0.0, shift], [0.0, 1.0, 0.0]], dtype=np.float32)
            if line_pos_x == "left" and line_pos_y == "bottom":
                checkpoint1 = cv.warpAffine(
                    finishline_mask,
                    M,
                    (finishline_mask.shape[1], finishline_mask.shape[0]),
                )
            else:
                checkpoint2 = cv.warpAffine(
                    finishline_mask,
                    M,
                    (finishline_mask.shape[1], finishline_mask.shape[0]),
                )

            M_rot = cv.getRotationMatrix2D((int(xs.mean()), int(ys.mean())), 90, 1)
            rotated_mask = cv.warpAffine(
                finishline_mask,
                M_rot,
                (finishline_mask.shape[1], finishline_mask.shape[0]),
            )

            kernel = cv.getStructuringElement(cv.MORPH_RECT, (1920, 1))
            rotated_mask = cv.dilate(rotated_mask, kernel, iterations=1)

            ys_r, xs_r = np.where(rotated_mask == 255)[:2]
            height = track_mask.shape[0]
            shift = abs(ys_r.min() - (height // 2))

            M_shift = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, shift]], dtype=np.float32)
            if line_pos_x == "left" and line_pos_y == "bottom":
                checkpoint2 = cv.warpAffine(
                    rotated_mask,
                    M_shift,
                    (rotated_mask.shape[1], rotated_mask.shape[0]),
                )
            else:
                checkpoint1 = cv.warpAffine(
                    rotated_mask,
                    M_shift,
                    (rotated_mask.shape[1], rotated_mask.shape[0]),
                )

        case "horizontal":
            ys, xs = np.where(finishline_mask == 255)[:2]

            M_rot = cv.getRotationMatrix2D((int(xs.mean()), int(ys.mean())), -90, 1)
            rotated_mask = cv.warpAffine(
                finishline_mask,
                M_rot,
                (finishline_mask.shape[1], finishline_mask.shape[0]),
            )

            kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1920))
            rotated_mask = cv.dilate(rotated_mask, kernel, iterations=1)
            ys, xs = np.where(rotated_mask == 255)
            line_left_point = xs.min() if xs.size > 0 else 0
            line_right_point = xs.max() if xs.size > 0 else 0

            cys, cxs = np.where(track_mask == 255)[:2]
            track_left_point = cxs.min() if cxs.size > 0 else 0
            track_right_point = cxs.max() if cxs.size > 0 else 0
            track_width = abs(track_right_point - track_left_point)

            shift = 0
            shift2 = 0
            # global line_pos_x
            match line_pos_x:
                case "left":
                    shift = -(0.5 * abs(line_left_point - track_right_point))
                    shift2 = 0.5 * abs(line_left_point - track_right_point)
                case "right":
                    shift = 0.5 * abs(line_left_point - track_left_point)
                    shift2 = -(0.5 * abs(line_left_point - track_left_point))

            M = np.array([[1.0, 0.0, shift], [0.0, 1.0, 0.0]], dtype=np.float32)
            checkpoint1 = cv.warpAffine(
                rotated_mask, M, (finishline_mask.shape[1], finishline_mask.shape[0])
            )

            M_shift = np.array([[1.0, 0.0, shift2], [0.0, 1.0, 0.0]], dtype=np.float32)
            checkpoint2 = cv.warpAffine(
                rotated_mask, M_shift, (rotated_mask.shape[1], rotated_mask.shape[0])
            )

        case _:
            raise ValueError(f"Unexpected orientation: {orientation}")

    cv.imwrite("Track data/checkpoint1.jpg", checkpoint1)
    cv.imwrite("Track data/checkpoint2.jpg", checkpoint2)


def race_analyze(player1, race_data=RaceData(1, False)):
    users = [player1]
    RESIZE_WIDTH = 1280
    RESIZE_HEIGHT = 640

    lock = threading.Lock()
    track = cv.imread("Track data/track_mask.jpg", cv.IMREAD_GRAYSCALE)
    line = cv.imread("Track data/finishline_mask.jpg", cv.IMREAD_GRAYSCALE)
    checkpoint1 = cv.imread("Track data/checkpoint1.jpg", cv.IMREAD_GRAYSCALE)
    checkpoint2 = cv.imread("Track data/checkpoint2.jpg", cv.IMREAD_GRAYSCALE)

    line = cv.resize(line, (RESIZE_WIDTH, RESIZE_HEIGHT))
    checkpoint1 = cv.resize(checkpoint1, (RESIZE_WIDTH, RESIZE_HEIGHT))
    checkpoint2 = cv.resize(checkpoint2, (RESIZE_WIDTH, RESIZE_HEIGHT))
    track = cv.resize(track, (RESIZE_WIDTH, RESIZE_HEIGHT))

    checkpoints = [
        line,
        checkpoint1,
        line,
        checkpoint2,
        checkpoint1,
        checkpoint2,
        line,
    ]
    if race_data.clockwise:
        checkpoints.reverse()

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_25H9)
    params = cv.aruco.DetectorParameters()

    params.cornerRefinementMethod = cv.aruco.CORNER_REFINE_SUBPIX
    params.cornerRefinementWinSize = 5  # Try 3-7
    params.cornerRefinementMaxIterations = 30
    params.cornerRefinementMinAccuracy = 0.1

    # Reduce minimum distance between markers to allow closer detection
    params.minMarkerDistanceRate = 0.05
    params.minMarkerPerimeterRate = 0.01

    # Loosen adaptive thresholding to cope with motion blur
    params.adaptiveThreshWinSizeMin = 3
    params.adaptiveThreshWinSizeMax = 23
    params.adaptiveThreshWinSizeStep = 10
    params.adaptiveThreshConstant = 7  # Slightly lower may help in low contrast

    # Enable perspective removal with relaxed parameters
    params.perspectiveRemoveIgnoredMarginPerCell = 0.13
    params.perspectiveRemovePixelPerCell = 8  # smaller = faster

    # Speed-vs-accuracy balance
    params.errorCorrectionRate = 0.6  # higher tolerates partial occlusion

    # Accept more candidates (may reduce false negatives)
    params.maxErroneousBitsInBorderRate = 0.45
    params.minOtsuStdDev = 5.0
    params.minCornerDistanceRate = 0.05

    detector = cv.aruco.ArucoDetector(aruco_dict, params)

    last_car = np.zeros((RESIZE_HEIGHT, RESIZE_WIDTH, 1), dtype=np.uint8)
    # last_car = cv.cvtColor(last_car, cv.COLOR_BGR2GRAY)

    while True:
        try:
            frame = frame_queue.get(timeout=1)
        except queue.Empty:
            continue
        frame = frame.copy()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        corners, ids, rejected = detector.detectMarkers(gray)
        for user in users:
            mask = np.zeros(gray.shape, dtype=np.uint8)

            if ids is not None:
                for i, marker_id in enumerate(ids.flatten()):
                    if marker_id == user.arucoID:
                        pts = corners[i][0].astype(np.int32)
                        cv.fillConvexPoly(mask, pts, (255, 255, 255))

            if cv.countNonZero(mask) > 0:
                last_car = mask
                if is_intersecting(last_car, track):
                    with lock:
                        user.is_on_track = True
                else:
                    with lock:
                        user.is_on_track = False

            if user.nextCheckpointIndex < len(checkpoints) and is_intersecting(
                last_car, checkpoints[user.nextCheckpointIndex]
            ):
                print("Crossed checkpoint ", user.nextCheckpointIndex)
                user.nextCheckpointIndex += 1
            if user.nextCheckpointIndex >= len(checkpoints):
                lapTimes = 0
                for time in user.lapTimes:
                    lapTimes += time
                user.lapTimes.append(user.raceTime - lapTimes)

                user.lapsCompleted += 1
                user.nextCheckpointIndex = 1
                if user.lapsCompleted == race_data.laps:
                    user.completedRace = True

        cv.imshow("Frame", last_car)
        # Exit on 'q' key press
        if cv.waitKey(1) & 0xFF == ord("q"):
            break


def race_loop(player1, race_data):
    user = player1
    vid_read = threading.Thread(target=read_frames, daemon=True)
    vid_analyze = threading.Thread(
        target=race_analyze, args=(player1, race_data), daemon=True
    )
    vid_read.start()
    vid_analyze.start()


def initialize_data():
    TRACK_PATH = "Track data/track_mask.jpg"
    FINISHLINE_PATH = "Track data/finishline_mask.jpg"

    POSSIBLE_IPS = ["192.168.129.140", "192.168.137.2"]

    for ip in POSSIBLE_IPS:
        if try_request(ip):
            break
    else:
        print("\033[91m[FAIL]\033[0m Could not reach the Raspberry Pi on any IP.")
        return
    frame = cv.imread("Track data/track.jpg")
    # frame = cv.resize(frame, (1280, 640))
    if not Path(TRACK_PATH).exists():
        track_mask = get_track_mask(frame)
        track_mask = cv.resize(track_mask, (1280, 640))
        cv.imwrite(TRACK_PATH, track_mask)
    if not Path(FINISHLINE_PATH).exists():
        line = get_finishline(frame)
        line = cv.resize(line, (1280, 640))
        cv.imwrite(FINISHLINE_PATH, line)
    if Path(TRACK_PATH).exists() and Path(FINISHLINE_PATH).exists():
        save_checkpoints()


if __name__ == "__main__":
    initialize_data()
