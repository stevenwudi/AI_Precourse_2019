"""
实现功能：
使用摄像头实时读取并进行人脸识别，q键退出，s键保存为图片
"""
import cv2
import time

cap = cv2.VideoCapture(0)

# 分类器位置：Anaconda3\Lib\site-packages\cv2\data
# 将分类器放在同一目录下，加载识别分类器
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

while True:
    # capture frame-by-frame
    ret, img = cap.read()

    # 转化为灰度图像，加快识别速度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3)

    for (x, y, w, h) in faces:  # 画出方框
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # 眼部识别
        # roi_gray = gray[y:y + h, x:x + w]
        # roi_color = img[y:y + h, x:x + w]
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex, ey, ew, eh) in eyes:
        #     cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # display the resulting frame
    cv2.imshow('face detect', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): # 按下q键时，退出
        break
    elif key == ord('s'): # 按下s键时，保存图片
        name = time.strftime("%Y%m%d%H%M%S", time.localtime())
        cv2.imwrite(name+'.jpg', img)

# when everything done, release the capture
cap.release()
cv2.destroyAllWindows()
