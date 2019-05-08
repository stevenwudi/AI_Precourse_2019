import cv2
pathf = './haarcascade_frontalface_default.xml'


def detect_face(filename):
    face_cascade = cv2.CascadeClassifier(pathf)
    face_cascade.load(pathf)
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('faces found', img)
    cv2.imwrite('faces_found_of_%s.jpg'%filename[0], img)
    cv2.waitKey(0)


if __name__ == '__main__':
    detect_face('a.jfif')
    detect_face('b.png' )
