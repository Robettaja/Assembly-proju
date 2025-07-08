import cv2 as cv
import threading
import cv2.aruco as aruco
import numpy as np
# from defisheye import Defisheye

line_pos_x = ""
line_pos_y = ""


def is_intersecting(mask1, mask2):
    return cv.countNonZero(cv.bitwise_and(mask1, mask2)) > 0


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

    # Define lower and upper bounds for red in HSV
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([160, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    # Create two masks and combine them
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv.bitwise_or(mask1, mask2)

    lower_blue = np.array([90, 45, 30])  # Lower hue, lower saturation and brightness
    upper_blue = np.array([140, 255, 255])  # Keep upper bound wide
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(image, lower_blue, upper_blue)
    dialite_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    dialated_mask = cv.dilate(red_mask, dialite_kernel, iterations=2)
    contours, hierarchy = cv.findContours(
        dialated_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
    )

    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
    parent_contour = sorted_contours[0]
    mask = np.zeros(image.shape, dtype=np.uint8)

    cv.drawContours(
        mask, [sorted_contours[0]], -1, (255, 255, 255), thickness=cv.FILLED
    )
    cv.drawContours(mask, [sorted_contours[2]], -1, (0, 0, 0), thickness=cv.FILLED)
    # cv.imshow("Track Mask", mask)
    return mask


def get_finishline(img):
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
            ys, xs, _ = np.where(finishline_mask == 255)

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

            cys, cxs, _ = np.where(track_mask == 255)
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


def race_loop(player1, player2=None):
    from race_main import set_user_intersection

    users = [player1]
    if player2:
        users.append(player2)
    RESIZE_WIDTH = 1920
    RESIZE_HEIGHT = 1080

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

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_25H9)
    parameters = cv.aruco.DetectorParameters()

    detector = cv.aruco.ArucoDetector(aruco_dict, parameters)
    video = cv.VideoCapture(1)
    video.set(cv.CAP_PROP_FRAME_WIDTH, RESIZE_WIDTH)
    video.set(cv.CAP_PROP_FRAME_HEIGHT, RESIZE_HEIGHT)
    ret, frame = video.read()
    last_car = np.zeros(frame.shape, dtype=np.uint8)
    last_car = cv.cvtColor(last_car, cv.COLOR_BGR2GRAY)

    while True:
        ret, frame = video.read()
        if not ret:
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        corners, ids, rejected = detector.detectMarkers(gray)
        for user in users:
            mask = np.zeros(gray.shape, dtype=np.uint8)

            if ids is not None:
                for i, marker_id in enumerate(ids.flatten()):
                    if marker_id == user.arucoID:
                        pts = corners[i][0].astype(np.int32)
                        cv.fillConvexPoly(mask, pts, (255, 255, 255))

                kernel = np.ones((9, 9), np.uint8)
                mask = cv.dilate(mask, kernel, iterations=2)

            if cv.countNonZero(mask) > 0:
                last_car = mask
                # last_car = cv.resize(last_car, (640, 480))
                if is_intersecting(mask, track):
                    with lock:
                        set_user_intersection(0, True)

            if user.nextCheckpointIndex < len(checkpoints) and is_intersecting(
                last_car, checkpoints[user.nextCheckpointIndex]
            ):
                user.nextCheckpointIndex += 1
            if user.nextCheckpointIndex >= len(checkpoints):
                user.completedRace = True

        cv.imshow("Frame", last_car)
        # Exit on 'q' key press
        if cv.waitKey(1) & 0xFF == ord("q"):
            break


def save_track_data():
    cap = cv.VideoCapture("rtsp://raspberrypi:8554/cam1", cv.CAP_FFMPEG)
    ret, frame = cap.read()
    track_mask = get_track_mask(frame)
    cv.imwrite("Track data/track_mask.jpg", track_mask)
    cv.imwrite("Track data/reference.jpg", frame)


def initialize_data():
    video = cv.VideoCapture(1)
    ret, frame = video.read()
    track_mask = get_track_mask(frame)
    cv.imwrite("Track data/track_mask.jpg", track_mask)
    line = get_finishline(frame)
    cv.imwrite("Track data/finishline_mask.jpg", line)
    cv.imwrite("Track data/reference.jpg", frame)
    save_checkpoints()


if __name__ == "__main__":
    save_track_data()
    # user1 = User(pygame.joystick.Joystick(0), "Player 1")
    # race_loop(user1, None)
