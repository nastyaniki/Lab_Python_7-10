import cv2

image = cv2.imread("variant-9.png")

if image is None:
    print("Не удалось открыть изображение.")
else:
    blue = image[:, :, 0]

    cv2.imshow("Original", image)
    cv2.imshow("Blue channel", blue)

    cv2.imwrite("blue_channel.png", blue)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(dictionary, parameters)

camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:

        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for marker in corners:

            points = marker[0]

            center_x = int(points[:, 0].mean())
            center_y = int(points[:, 1].mean())

            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            if center_x > frame.shape[1] // 2:
                cv2.putText(frame,
                            "RIGHT HALF",
                            (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2)

    cv2.line(frame,
             (frame.shape[1] // 2, 0),
             (frame.shape[1] // 2, frame.shape[0]),
             (255, 0, 0),
             2)

    cv2.imshow("ArUco Detection", frame)

    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()