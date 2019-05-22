import cv2
import sys

def detect():
    face_casade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    camera=cv2.VideoCapture(0)  #0代表调用默认摄像头，1代表调用外接摄像头
    #i=1
    while (True):
        ret,frame=camera.read()

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_casade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            img=cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray=gray[y:y+h,x:x+w]
        cv2.imshow("camera",frame)
        #if i<=3:
        #    cv2.imwrite('frame_0%d.jpg'%i, frame)
        #    i+=1#保存连续的三帧

        key=cv2.waitKey(1) & 0xff
        if key==ord('q'):
            break
    camera.release()#
    cv2.destroyAllWindows()#

if  __name__=="__main__":
    detect()
