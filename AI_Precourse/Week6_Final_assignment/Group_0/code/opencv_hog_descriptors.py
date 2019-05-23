import dlib
import cv2
import numpy as np

# winSize = (64,64)
# blockSize = (16,16)
# blockStride = (8,8)
# cellSize = (8,8)
# nbins = 9
# derivAperture = 1
# winSigma = 4.
# histogramNormType = 0
# L2HysThreshold = 2.0000000000000001e-01
# gammaCorrection = 0
# nlevels = 64
# hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
#                         histogramNormType,L2HysThreshold,gammaCorrection,nlevels)
hog = cv2.HOGDescriptor()
cap = cv2.VideoCapture(0)

# hand position
hand_pos = [50, 150, 150, 250]
dist_threshold = 610

## dlib correlation tracker
tracker = dlib.correlation_tracker()

## load saved hand hog file
hand_hog = np.loadtxt('hand_hog.txt')
track_flag = False

while(cap.isOpened()):
    ret, img = cap.read()
    if not track_flag:
        cv2.rectangle(img,(hand_pos[2],hand_pos[3]),(hand_pos[0],hand_pos[1]),(0,255,0),0)
        crop_img = img[hand_pos[1]:hand_pos[3], hand_pos[0]:hand_pos[2]]
        #compute(img[, winStride[, padding[, locations]]]) -> descriptors
        winStride = (8,8)
        padding = (8,8)
        locations = (((hand_pos[2]+hand_pos[0])/2.,(hand_pos[3]+hand_pos[1])/2.),)
        hist = hog.compute(img,winStride,padding,locations)

        cv2.imshow('Gesture', img)
        cv2.imshow('hand', crop_img)
        dist =np.linalg.norm(hand_hog - hist)
        print(dist)
        if dist < dist_threshold:
            # 240 is a reasonable guess, we found the hand! Start tracking!
            tracker.start_track(img, dlib.rectangle(hand_pos[0], hand_pos[1], hand_pos[2], hand_pos[3]))
            track_flag = True
    else:
        tracker.update(img)
        pos = tracker.get_position()
        cv2.rectangle(img,(int(pos.right()), int(pos.bottom())),(int(pos.left()), int(pos.top())),(255,0,0),0)
        left = max(0, int(pos.left()))
        right = min(img.shape[0], int(pos.right()))
        top = max(0, int(pos.top()))
        bottom = min(img.shape[1], int(pos.bottom()))
        crop_img = img[top:bottom, left:right]
        cv2.imshow('Gesture', img)
        cv2.imshow('hand', crop_img)

    k = cv2.waitKey(10)
    if k == ord('s'):
        cv2.imwrite('image/myhand.png', crop_img)
        np.savetxt('hand_hog.txt', hist)
        break
    if k == 27:
        break