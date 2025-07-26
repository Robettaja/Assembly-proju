import cv2 as cv
import subprocess
import tempfile
import numpy as np
import threading
import queue
from defisheye import Defisheye

# process = None

# process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)


frame_queue = queue.Queue(maxsize=5)


def read_frames():
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
        "-vsync",
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
        if process.stdout:
            raw_frame = process.stdout.read(frame_size)
            if len(raw_frame) != frame_size:
                print("Frame incomplete or stream ended")
                break

            frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height, width, 3))
            try:
                frame_queue.put_nowait(frame)
            except queue.Full:
                try:
                    frame_queue.get_nowait()
                    frame_queue.put_nowait(frame)
                except queue.Full:
                    pass


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

tag = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_APRILTAG_25H9)
detector = cv.aruco.ArucoDetector(tag, params)


def aruco(frame):
    corners, ids, rejected = detector.detectMarkers(frame)

    # Create an empty binary mask (same size as frame, single channel)
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)

    if ids is not None:
        # Draw white filled polygons over detected marker areas in the mask
        for marker_corners in corners:
            int_corners = np.int32(marker_corners)
            cv.fillPoly(mask, int_corners, 255)

    return mask


def black(frame):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define HSV range for black
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])  # Adjust V upper limit if needed

    # Create mask for black
    mask = cv.inRange(hsv, lower_black, upper_black)
    return mask


def detect_aruco():
    while True:
        try:
            frame = frame_queue.get(timeout=1)
        except queue.Empty:
            continue
        frame = frame.copy()
        corners, ids, rejected = detector.detectMarkers(frame)
        if ids is not None:
            cv.aruco.drawDetectedMarkers(frame, corners, ids)

        cv.imshow("Aruco", frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break


# Start threads
thread_read = threading.Thread(target=read_frames, daemon=True)
thread_detect = threading.Thread(target=detect_aruco, daemon=True)

thread_read.start()
thread_detect.start()

# Keep main thread alive until detection thread ends
thread_detect.join()
# Clean up

cv.destroyAllWindows()
