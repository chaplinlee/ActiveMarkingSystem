# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import cv2
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import itertools
from sklearn.metrics import confusion_matrix
from theano import ifelse
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras import regularizers

import scipy.misc
K.set_image_dim_ordering('th')  

def larger_model2():
    model = Sequential()
    model.add(Conv2D(20, (5, 5), input_shape=(3,100, 100), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(11, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(30, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    return model

def softmax(x):
    return np.exp(x)/np.sum(np.exp(x),axis=0)

def filling_rect(img,start_x,start_y,col,row,color):
    for i in range(col):
        for j in range(row):
            img[i+start_x][j+start_y] = color

def find_max(list):
	index= 0
	max = list[0]
	for i in range(len(list)):
		if list[i] > max:
			index= i
			max = list[i]	
	return (index)

def confirm_species(list):
	index = 0
	
		
 #load data
path = "../hu_test/CNNdatas/test/concrete/11.jpg"
num_classes = 2
curr = cv2.imread(path)
#temp_image = curr[0:2000,2400:4000]
plt.imshow(curr)
plt.show()
#scipy.misc.imsave('map_real.jpg', temp_image)	
width = curr.shape[1] 
height = curr.shape[0]
data = "cnn_data"
imgs = {}
# reshape to be [samples][pixels][width][height]

#load model
model2 = keras.models.load_model('cnn_base_model')

#init 
size = 100
width =  size*(width/size)
height = size*(height/size)
dict1={}
grass_color = [0,255,0]
concrete_color = [160,82,45]
pave_color= [255,165,0]
unknown_color = [255,255,255]

dict1[0] = grass_color
dict1[1] = concrete_color
dict1[2] = pave_color
dict1[3] = unknown_color

img = np.zeros((height,width,3),np.uint8)#生成一个空彩色图像	

for i in range(height/size):
  for j in range(width/size):
    X_test = curr[i*size:i*size+size,j*size:j*size+size]
    b, g, r = X_test[:,:,0], X_test[:,:,1], X_test[:,:,2]
    x = np.stack((r, g, b), axis=0) # reorder to rgb
    imgs[data] = [x]
    X_tmp = np.array(imgs['cnn_data']).astype('float32')/255.0
    Y_pred_vecs = model2.predict(X_tmp, verbose=1)
    print(Y_pred_vecs[0])
    judge = find_max(Y_pred_vecs[0])
    print(judge)
    filling_rect(img,i*size,j*size,size,size,dict1[judge])

scipy.misc.imsave('map_gen.jpg', img)	




