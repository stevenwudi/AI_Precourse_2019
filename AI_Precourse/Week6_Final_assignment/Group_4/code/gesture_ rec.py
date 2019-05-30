"""
实现功能：
使用摄像头实时读取并进行剪刀石头布判别，q键退出，s键保存为图片
"""
import cv2
import time
import numpy as np
import math


# 移除视频数据的背景噪声
def _remove_background(frame):
    fgbg = cv2.createBackgroundSubtractorMOG2() # 利用BackgroundSubtractorMOG2算法消除背景
    # fgmask = bgModel.apply(frame)
    fgmask = fgbg.apply(frame)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res

# 视频数据的人体皮肤检测
def _bodyskin_detetc(frame):
    # 肤色检测: YCrCb之Cr分量 + OTSU二值化
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb) # 分解为YUV图像,得到CR分量
    (_, cr, _) = cv2.split(ycrcb)
    cr1 = cv2.GaussianBlur(cr, (5, 5), 0) # 高斯滤波
    _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # OTSU图像二值化
    return skin

# 检测图像中的凸点(手指)个数
def _get_contours(array):
    # 利用findContours检测图像中的轮廓, 其中返回值contours包含了图像中所有轮廓的坐标点
    contours, _ = cv2.findContours(array, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    return contours

# 根据图像中凹凸点中的 (开始点, 结束点, 远点)的坐标, 利用余弦定理计算两根手指之间的夹角, 其必为锐角, 根据锐角的个数判别手势.
def _get_defects_count(array, contour, defects, verbose=False):
    ndefects = 0

    for i in range(defects.shape[0]):
        s, e, f, _ = defects[i, 0]
        beg = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])
        a = _get_eucledian_distance(beg, end)
        b = _get_eucledian_distance(beg, far)
        c = _get_eucledian_distance(end, far)
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # * 57

        if angle <= math.pi / 2:  # 90:
            ndefects = ndefects + 1

            if verbose:
                cv2.circle(array, far, 3, _COLOR_RED, -1)

        if verbose:
            cv2.line(array, beg, end, _COLOR_RED, 1)

    return array, ndefects


def grdetect(array, verbose=False):
    copy = array.copy()
    array = _remove_background(array)  # 移除背景噪声
    thresh = _bodyskin_detetc(array)   # 人体皮肤检测

    contours = _get_contours(thresh.copy())  # 计算图像的轮廓

    largecont = max(contours, key=lambda contour: cv2.contourArea(contour))

    hull = cv2.convexHull(largecont, returnPoints=False)  # 计算轮廓的凸点
    defects = cv2.convexityDefects(largecont, hull)  # 计算轮廓的凹点

    if defects is not None:
        # 利用凹陷点坐标, 根据余弦定理计算图像中锐角个数
        copy, ndefects = _get_defects_count(copy, largecont, defects, verbose=verbose)

        # 根据锐角个数判断手势, 会有一定的误差
        return ndefects

def _get_eucledian_distance(a, b):
    distance = math.sqrt( (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return distance


cap = cv2.VideoCapture(0)

while True:
    # capture frame-by-frame
    ret, img = cap.read()

    img = _remove_background(img)

    # 画出两个限制方框
    cv2.rectangle(img, (70, 220), (270, 420), (255, 0, 0), 2)
    cv2.rectangle(img, (370, 220), (570, 420), (255, 0, 0), 2)

    # 取出方框内容
    geture1 = img[220:420, 70:270]
    geture2 = img[220:420, 370:570]

    # 计算锐角个数
    event1 = grdetect(geture1)
    event2 = grdetect(geture2)

    print(event1, event2)

    # 判断手势类型
    judge = ['rock', 'scissors', 'paper']
    if event1 <= 1:
        player1 = 0
    elif event1 <= 3:
        player1 = 1
    elif event1 >= 4:
        player1 = 2
    cv2.putText(img, "PLAYER1:"+judge[player1], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    if event2 <= 1:
        player2 = 0
    elif event2 <= 3:
        player2 = 1
    elif event2 >= 4:
        player2 = 2
    cv2.putText(img, "PLAYER1:" + judge[player2], (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    # 判断输赢
    if player1 == player2:
        cv2.putText(img, " DRAW!", (230, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
    elif player1 < player2 and (player2 - player1) == 1 or player1 > player2 and (player1 - player2) == 2:
        cv2.putText(img, "PLAYER1 win!", (220, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
    else:
        cv2.putText(img, "PLAYER2 win!", (220, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    # display the resulting frame
    cv2.namedWindow('gesture', cv2.WINDOW_NORMAL)
    cv2.imshow('gesture', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # 按下q键时，退出
        break
    elif key == ord('s'):  # 按下s键时，保存图片
        name = time.strftime("%Y%m%d%H%M%S", time.localtime())
        cv2.imwrite(name+'.jpg', img)

# when everything done, release the capture
cap.release()
cv2.destroyAllWindows()
