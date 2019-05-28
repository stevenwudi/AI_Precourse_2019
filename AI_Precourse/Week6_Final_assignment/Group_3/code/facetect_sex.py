# -*- coding:utf-8 -*-

from PIL import Image
import sys
import dlib
import cv2
import os
import os.path
import numpy as np
import PIL.Image
from pylab import *
import time

def get_face_from_photo(i,path,spath):
    detector = dlib.get_frontal_face_detector() #获取人脸分类
    # 读取path路径下的图片，获得所有的图片名字
    filenames = os.listdir(path)
    for f1 in filenames:
        f = os.path.join(path,f1)
        iimag = PIL.Image.open(f)
        # opencv 读取图片，并显示
        img = cv2.imread(f, cv2.IMREAD_COLOR)
        b, g, r = cv2.split(img)    # 分离三个颜色通道
        img2 = cv2.merge([r, g, b])   # 生成新图片
        counts = detector(img, 1) #人脸检测 

        for index, face in enumerate(counts):

            # 在图片中标注人脸，并显示
            left = face.left()
            top = face.top()
            right = face.right()
            bottom = face.bottom()

            #保存人脸区域
            j =str(i)
            j = j+'.jpg'
            save_path = os.path.join(spath,j)
            region = (left,top,right,bottom)
            #裁切图片
            cropImg = iimag.crop(region)

            #保存裁切后的图片
            cropImg.save(save_path)
            i +=1

            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)
            cv2.namedWindow(f, cv2.WINDOW_AUTOSIZE)
            cv2.imshow(f, img)
    # 销毁窗口
    cv2.destroyAllWindows()
    return i


def change_photo_size28(path,spath):
    '''
    将人脸图片转化为28*28的灰度图片
    '''
    filenames = os.listdir(path)

    for filename in filenames:
        f = os.path.join(path,filename)
        iimag = PIL.Image.open(f).convert('L').resize((28,28))
        savepath = os.path.join(spath,filename)
        iimag.save(savepath)


def read_photo_for_train(photo_path):
    '''
    读取训练图片
    '''
    k=0
    filenames = os.listdir(photo_path)
    for filename in filenames:
        k+=1
    for i in range(k):
        j = i
        j = str(j)
        st = '.jpg'
        j = j+st
        j = os.path.join(photo_path,j)
        im1 = array(Image.open(j).convert('L'))
        #（28，28）-->(28*28,1)
        im1 = im1.reshape((784,1))
        #把所有的图片灰度值放到一个矩阵中
        #一列代表一张图片的信息
        if i == 0:
            im = im1
        else:
            im = np.hstack((im,im1))
    return im,k


def layerout(w,b,x):

    '''
    sigmoid函数实现
    '''

    y = np.dot(w,x) + b
    t = -1.0*y
    # n = len(y)
    # for i in range(n):
        # y[i]=1.0/(1+exp(-y[i]))
    y = 1.0/(1+exp(t))
    return y


def mytrain(step,alpha,hid,k,x_train,y_train):
    a = alpha
    inn = 784  #输入神经元个数
    out = 1  #输出层神经元个数

    w = np.random.randn(out,hid)
    w = np.mat(w)
    b = np.mat(np.random.randn(out,1)) 
    w_h = np.random.randn(hid,inn)
    w_h = np.mat(w_h)
    b_h = np.mat(np.random.randn(hid,1)) 

    for i in range(step):
        #打乱训练样本
        r=np.random.permutation(k)
        x_train = x_train[:,r]
        y_train = y_train[:,r]
        #batch_size
        for j in range(k-2):
            x = np.mat(x_train[:,j]) 
            x = x.reshape((784,1))
            y = np.mat(y_train[:,j]) 
            y = y.reshape((1,1))
            hid_put = layerout(w_h,b_h,x) 
            out_put = layerout(w,b,hid_put) 

            #更新公式的实现
            o_update = np.multiply(np.multiply((y-out_put),out_put),(1-out_put)) 
            h_update = np.multiply(np.multiply(np.dot((w.T),np.mat(o_update)),hid_put),(1-hid_put)) 

            outw_update = a*np.dot(o_update,(hid_put.T)) 
            outb_update = a*o_update 
            hidw_update = a*np.dot(h_update,(x.T)) 
            hidb_update = a*h_update 

            w = w + outw_update 
            b = b+ outb_update 
            w_h = w_h +hidw_update 
            b_h =b_h +hidb_update 

    return w,b,w_h,b_h

def mytest(i,x_test,w,b,w_h,b_h):
    '''
    预测结果pre>0.5，为male；预测结果pre<=0.5,为female
    '''
    hid = layerout(w_h,b_h,x_test)
    pre = layerout(w,b,hid)
    #print(pre)
    if pre > 0.5:
        #print('photo:%d,This is a man!'%i)
        return 1
    else:
        #print('photo:%d,This is a woman!'%i)
        return 0


###图片处理###
#框出人脸，并保存到faces中,i为保存的名字
i = 0
#remale
path = '.\\photos\\female'
spath = '.\\photos\\faces'
i = get_face_from_photo(i,path,spath)
woman_number = i
print('woman_number:%d'%woman_number)
#male
path = '.\\photos\\male'
i = get_face_from_photo(i,path,spath)
man_number = i - woman_number
print('man_number:%d'%man_number)
#将人脸图片转化为28*28的灰度图片
path = '.\\photos\\faces'
spath = '.\\photos\\faces'
change_photo_size28(path,spath)

###测试图片处理###
#框出人脸，并保存到femaletests中,i为保存的名字
i = 0
#female测试集
path = '.\\photos\\femaletest'
spath = '.\\photos\\femaletests'
i = get_face_from_photo(i,path,spath)
#将人脸图片转化为28*28的灰度图片
path = '.\\photos\\femaletests'
spath = '.\\photos\\femaletests'
change_photo_size28(path,spath)

#框出人脸，并保存到maletests中,i为保存的名字
i = 0
#male测试集
path = '.\\photos\\maletest'
spath = '.\\photos\\maletests'
i = get_face_from_photo(i,path,spath)
#将人脸图片转化为28*28的灰度图片
path = '.\\photos\\maletests'
spath = '.\\photos\\maletests'
change_photo_size28(path,spath)


woman_number = int(input("please input female_number:"))
man_number = int(input("please input male_number:"))
step=int(input('mytrain迭代步数：')) 
alpha=double(input('学习因子：')) 
hid = int(input('隐藏层神经元个数：'))#隐藏层神经元个数
starttime = time.time()
###训练###
#获取图片信息
spath = '.\\photos\\faces'
im,k = read_photo_for_train(spath)

#归一化
immin = im.min()
immax = im.max()
im = (im-immin)/(immax-immin)

x_train = im

#制作标签,标签0为female,标签1为male
y1 = np.zeros((1,woman_number))
y2 = np.ones((1,man_number))
y_train = np.hstack((y1,y2))

#开始训练
print("----------------------开始训练-----------------------------")
w,b,w_h,b_h = mytrain(step,alpha,hid,k,x_train,y_train)
print("-----------------------训练结束----------------------------")


#测试
print("--------------------测试女生-------------------------------")


spath = '.\\photos\\femaletests'
#获取图片信息
im,k = read_photo_for_train(spath)

#归一化
immin = im.min()
immax = im.max()
im = (im-immin)/(immax-immin)

x_test = im
female_num = 0
for i in range(k):
    xx = x_test[:,i]
    xx = xx.reshape((784,1))
    y = mytest(i,xx,w,b,w_h,b_h)
    if y == 0:
        female_num += 1
acc = female_num / k
print('female test_accuracy:%.4f'%acc)
print("---------------------测试男生-----------------------------")


spath = '.\\photos\\maletests'
#获取图片信息
im,k = read_photo_for_train(spath)

#归一化
immin = im.min()
immax = im.max()
im = (im-immin)/(immax-immin)

x_test = im
male_num = 0
for i in range(k):
    xx = x_test[:,i]
    xx = xx.reshape((784,1))
    y = mytest(i,xx,w,b,w_h,b_h)
    if y == 0:
        male_num += 1
acc = male_num / k
print('male test_accuracy:%.4f'%acc)
endtime = time.time()
print("time:%.4fs"%(endtime-starttime))
