# -*- coding: utf-8 -*-
"""
Created on Wed May  8 17:06:49 2019

@author: Administrator
"""
#图片中四个人脸，检测出三个，hara feature 可能不太完善

import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+w),(0,0,255),2)
    
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.imwrite('processedImage.jpg',img)
cv2.destroyAllWindows()
