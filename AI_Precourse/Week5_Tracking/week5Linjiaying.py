import cv2
import imutils

tracker = cv2.TrackerKCF_create()
vs = cv2.VideoCapture(0)
init1 = None
while True:
    frame = vs.read()
    frame = frame[1]
    if frame is None:
        break
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]

    if init1 is not None:

        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)

        fps.update()
        fps.stop()

        info = [
            ("Tracker"," kcf"),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]

        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        key = cv2.waitKey(1)
        if key == ord("s"):
            break;

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

