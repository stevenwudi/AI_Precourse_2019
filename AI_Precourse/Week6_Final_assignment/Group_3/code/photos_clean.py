# -*- coding: utf-8 -*-
import os
import cv2
from PIL import Image
from PIL import ImageFile
import dlib
import threading
ImageFile.LOAD_TRUNCATED_IMAGES = True

def process_img(path, new_path):
    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    dirs = os.listdir(path)
    detector = dlib.get_frontal_face_detector()
    j = 0
    i = 0
    for pic_dir in dirs:
        dir_path = path+'//'+pic_dir
        i += 1
        pics = os.listdir(dir_path)
        for pic in pics:
            image_Path = dir_path+'//'+pic
            image = cv2.imread(image_Path,0)
            if image is None:
                break
            counts = detector(image, 1)
            if len(counts) == 0:
                break
            img = Image.open(image_Path)
            if i <40:
                new_pic_path = new_path[0]
            else:
                new_pic_path = new_path[1]
            if not os.path.exists(new_pic_path):
                os.makedirs(new_pic_path)
            if len(img.split()) == 4:
                # 利用split和merge将通道从四个转换为三个
                r, g, b, a = img.split()
                toimg = Image.merge("RGB", (r, g, b))
                toimg.save(new_pic_path + '//' + str(j) + '.jpg')
                j += 1
            else:
                try:
                    img.save(new_pic_path + '//' + str(j) + '.jpg')
                    j += 1
                except:
                    continue
        print('Finish......!')
 
def lock_test(path, new_path):
    mu = threading.Lock()
    if mu.acquire(True):
        process_img(path, new_path)
        mu.release()
 
if __name__ == '__main__':
    paths = [r'.//Star//maleStar',r'.//Star//femaleStar']
    new_paths = [[r'.//photos//male', r'.//photos//maletest'],[r'.//photos//female', r'.//photos//femaletest']]
    for i in range(len(paths)):
        my_thread = threading.Thread(target=lock_test, args=(paths[i], new_paths[i]))
        my_thread.start()