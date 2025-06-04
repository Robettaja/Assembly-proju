import cv2
import numpy as np
import cv2.aruco as aruco

# Function to adjust the gamma of an image
def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

# Function to detect and highlight red contours in the video feed
def track_red_contours():
    # Capture video from the default camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video feed
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = adjust_gamma(frame, gamma=1)

        # --- ArUco marker detection ---
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_MIP_36h12)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejected = detector.detectMarkers(frame)
        if ids is not None:
            for i, corner in enumerate(corners):
                pts = corner[0].astype(int)
                # Draw red box
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=3)
                # Draw black ID at the top-left corner of the marker
                cX, cY = pts[0][0], pts[0][1]
                cv2.putText(frame, str(ids[i][0]), (cX, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

        # --- Blue area detection as before ---
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 150, 70])
        upper_blue = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_uint8 = mask.astype(np.uint8)
        contours, _ = cv2.findContours(mask_uint8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        if len(contours) >= 3:
            idx1, idx2 = 1, 2  # Change these indices as needed for your drawing
            mask_outer = np.zeros_like(mask)
            mask_inner = np.zeros_like(mask)
            cv2.drawContours(mask_outer, [contours[idx1]], -1, (255,), -1)
            cv2.drawContours(mask_inner, [contours[idx2]], -1, (255,), -1)
            area_mask = cv2.subtract(mask_outer, mask_inner)
            frame[area_mask == 255] = [0, 255, 255]  # Yellow in BGR

        for contour in contours:
            if cv2.contourArea(contour) > 0.1:
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

        cv2.imshow('Blue Contour Tracker + ArUco', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Run the blue contour tracker
if __name__ == "__main__":
    track_red_contours()
