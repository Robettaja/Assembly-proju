import cv2 as cv
import cv2.aruco as aruco
import time
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
from defisheye import Defisheye


def aruco_detect(img, aruco_mark_type):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.GaussianBlur(img, (5, 5), 0)
    aruco_dict = aruco.getPredefinedDictionary(aruco_mark_type)
    parameters = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(img)
    mask = np.zeros(img.shape, dtype=np.uint8)
    if ids is not None:
        for marker_corners in corners:
            pts = marker_corners[0].astype(np.int32)
            cv.fillConvexPoly(mask, pts, 255)
    return mask


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
    lower_blue = np.array([90, 45, 30])  # Lower hue, lower saturation and brightness
    upper_blue = np.array([140, 255, 255])  # Keep upper bound wide
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(image, lower_blue, upper_blue)
    dialite_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    dialated_mask = cv.dilate(mask, dialite_kernel, iterations=2)
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

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
    track = cv.imread("Track data/track_mask.jpg", cv.IMREAD_GRAYSCALE)
    ys, xs, _ = np.where(track == 255)

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
                kernel_width = int(0.4 * w)
                kernel = cv.getStructuringElement(
                    cv.MORPH_RECT, (kernel_width, kernel_height)
                )
            case "vertical":
                kernel_height = int(0.4 * h)
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

    orientation = get_line_orientation(
        finishline_mask
    )  # expects 'horizontal' or 'vertical'

    match orientation:
        case "vertical":
            line_location = white_pixels_side(finishline_mask, axis="y")
            ys, xs, _ = np.where(finishline_mask == 255)
            line_top_point = ys.min() if ys.size > 0 else 0

            cys, cxs, _ = np.where(track_mask == 255)
            track_top_point = cys.min() if cys.size > 0 else 0
            track_bottom_point = cys.max() if cys.size > 0 else 0

            shift_y = 0
            match line_location:
                case "top":
                    shift_y = track_bottom_point - line_top_point
                case "bottom":
                    shift_y = -(line_top_point - track_top_point)

            M = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, shift_y]], dtype=np.float32)
            checkpoint2 = cv.warpAffine(
                finishline_mask, M, (finishline_mask.shape[1], finishline_mask.shape[0])
            )

            M_rot = cv.getRotationMatrix2D((int(xs.mean()), int(ys.mean())), 90, 1)
            rotated_mask = cv.warpAffine(
                finishline_mask,
                M_rot,
                (finishline_mask.shape[1], finishline_mask.shape[0]),
            )

            new_shift_y = shift_y // 2
            M_shift = np.array(
                [[1.0, 0.0, 0.0], [0.0, 1.0, new_shift_y]], dtype=np.float32
            )
            rotated_mask = cv.warpAffine(
                rotated_mask, M_shift, (rotated_mask.shape[1], rotated_mask.shape[0])
            )

            ys_r, xs_r = np.where(rotated_mask == 255)
            width = xs_r.max() - xs_r.min()
            x_offset = cxs.max() - xs_r.max() + (width // 2)
            M1 = np.array([[1.0, 0.0, x_offset], [0.0, 1.0, 0]], dtype=np.float32)
            checkpoint1 = cv.warpAffine(
                rotated_mask, M1, (rotated_mask.shape[1], rotated_mask.shape[0])
            )

            x_offset = -(xs_r.min() - cxs.min() + (width // 2))
            M3 = np.array([[1.0, 0.0, x_offset], [0.0, 1.0, 0]], dtype=np.float32)
            checkpoint3 = cv.warpAffine(
                rotated_mask, M3, (rotated_mask.shape[1], rotated_mask.shape[0])
            )

        case "horizontal":
            line_location = white_pixels_side(finishline_mask, axis="x")
            ys, xs, _ = np.where(finishline_mask == 255)
            height = ys.max() - ys.min()
            width = xs.max() - xs.min()
            line_left_point = xs.min() if xs.size > 0 else 0
            line_right_point = xs.max() if xs.size > 0 else 0

            cys, cxs, _ = np.where(track_mask == 255)
            track_left_point = cxs.min() if cxs.size > 0 else 0
            track_right_point = cxs.max() if cxs.size > 0 else 0

            shift_x = 0
            match line_location:
                case "left":
                    shift_x = abs(track_right_point - line_left_point) - (width // 2)
                case "right":
                    shift_x = -(abs(track_left_point - line_left_point) + (height // 2))
            M = np.array([[1.0, 0.0, shift_x], [0.0, 1.0, 0.0]], dtype=np.float32)
            checkpoint2 = cv.warpAffine(
                finishline_mask, M, (finishline_mask.shape[1], finishline_mask.shape[0])
            )

            M_rot = cv.getRotationMatrix2D((int(xs.mean()), int(ys.mean())), -90, 1)
            rotated_mask = cv.warpAffine(
                finishline_mask,
                M_rot,
                (finishline_mask.shape[1], finishline_mask.shape[0]),
            )

            new_shift_x = shift_x // 2
            M_shift = np.array(
                [[1.0, 0.0, new_shift_x], [0.0, 1.0, 0.0]], dtype=np.float32
            )
            rotated_mask = cv.warpAffine(
                rotated_mask, M_shift, (rotated_mask.shape[1], rotated_mask.shape[0])
            )

            ys_r, xs_r = np.where(rotated_mask == 255)
            width = xs_r.max() - xs_r.min()
            y_offset = cys.max() - ys_r.max() + (width // 2)
            M1 = np.array([[1.0, 0.0, 0], [0.0, 1.0, y_offset]], dtype=np.float32)
            checkpoint1 = cv.warpAffine(
                rotated_mask, M1, (rotated_mask.shape[1], rotated_mask.shape[0])
            )

            y_offset = -(ys_r.min() - cys.min() + (width // 2))
            M3 = np.array([[1.0, 0.0, 0], [0.0, 1.0, y_offset]], dtype=np.float32)
            checkpoint3 = cv.warpAffine(
                rotated_mask, M3, (rotated_mask.shape[1], rotated_mask.shape[0])
            )

        case _:
            raise ValueError(f"Unexpected orientation: {orientation}")

    cv.imwrite("Track data/checkpoint1.jpg", checkpoint1)
    cv.imwrite("Track data/checkpoint2.jpg", checkpoint2)
    cv.imwrite("Track data/checkpoint3.jpg", checkpoint3)


def race_loop():
    line = cv.imread("Track data/finishline_mask.jpg", cv.IMREAD_GRAYSCALE)

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_25H9)
    parameters = cv.aruco.DetectorParameters()

    detector = cv.aruco.ArucoDetector(aruco_dict, parameters)
    video = cv.VideoCapture(1)
    video.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
    video.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
    ret, frame = video.read()
    last_car = np.zeros(frame.shape, dtype=np.uint8)

    while True:
        timer = time.time()
        ret, frame = video.read()
        if not ret:
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        corners, ids, rejected = detector.detectMarkers(gray)

        mask = np.zeros(frame.shape, dtype=np.uint8)
        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)

        if ids is not None:
            for marker_corners in corners:
                pts = marker_corners[0].astype(np.int32)
                cv.fillConvexPoly(mask, pts, (255, 255, 255))
                kernel = np.ones((9, 9), np.uint8)
                mask = cv.dilate(mask, kernel, iterations=2)
        if cv.countNonZero(mask) > 0:
            last_car = mask
        fps = 1 / (time.time() - timer)
        cv.putText(
            last_car,
            f"FPS: {fps:.2f}",
            (10, 30),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )
        # last_car = cv.resize(last_car, (640, 480))
        # if is_intersecting(last_car, line):
        #     print("Finish line crossed!")

        cv.imshow("Frame", last_car)
        # Exit on 'q' key press
        if cv.waitKey(1) & 0xFF == ord("q"):
            break


def track_test_loop():
    video = cv.VideoCapture(1)
    ret, frame = video.read()
    track_mask = get_track_mask(frame)
    cv.imwrite("Track data/track_mask.jpg", track_mask)
    line = get_finishline(frame)
    cv.imwrite("Track data/finishline_mask.jpg", line)


track_test_loop()
save_checkpoints()
# race_loop()
