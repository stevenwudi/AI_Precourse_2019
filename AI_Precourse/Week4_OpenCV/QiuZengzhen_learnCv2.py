import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse

from imutils.video import VideoStream

cap = cv2.VideoCapture(0)
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("myself.jpg", frame)
        break
cap.release()
cv2.destroyAllWindows()



img_path = 'kobe.jpg'
# 载入带有人脸的图片
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 载入人脸检测的Cascade模型
FaceCascade = cv2.CascadeClassifier('D:\python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
# 检测画面中的人脸
faces,rl,wl = FaceCascade.detectMultiScale3(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    outputRejectLevels=True
)
print(wl)
print(rl)
# 遍历返回的face数组
for face in faces:
    # 解析tuple类型的face位置数据
    # (x, y): 左上角坐标值
    # w: 人脸矩形区域的宽度
    # h: 人脸矩形区域的高度
    (x, y, w, h) = face
    # 在原彩图上绘制矩形
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 4)

# 创建一个窗口 名字叫做Face
cv2.imwrite("faceDection.jpg",img)
cv2.namedWindow('Face',flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)

# 在窗口Face上面展示图片img
cv2.imshow('Face', img)
# 等待任意按键按下
cv2.waitKey(0)
# 关闭所有的窗口
cv2.destroyAllWindows()

