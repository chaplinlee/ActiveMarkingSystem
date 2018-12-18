#-*- coding: utf-8 -*- 
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
import random
from random import choice
import scipy.misc
K.set_image_dim_ordering('th')  

def larger_model2():
    model = Sequential()
    model.add(Conv2D(20, (5, 5), input_shape=(3, 100, 100), activation='relu'))
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

'''
active learning alothgim
'''
		
def cross_entroy(x):
    loss = -np.sum(x*np.log(x))
    #print(x[0]*np.log(x[0])+x[1]*np.log(x[1])+x[2]*np.log(x[2]))
    print(loss)
    return loss
        
def Al_query(input_pro,k):
        list_k={}
        print(len(input_pro))
        for i in range(len(input_pro)):
		list_k[input_pro[i][0]] = input_pro[i][1]		
	print(list_k)
	list_k = sorted(list_k.items(), key = lambda k: k[1],reverse = True)
        print("AL========================")
	print(list_k[0:k])
        for key in list_k[0:k]:
		print key[0]
	return(list_k[0:k])


def random_query(input_pro,k):
        list_k={}
        for i in range(len(input_pro)):
		list_k[input_pro[i][0]] = input_pro[i][1]		

	list_k = sorted(list_k.items(), key = lambda k: k[1],reverse = True)
	slice = random.sample(list_k, k) 
	print(slice)
	return(slice)

def put_data(data,list_k):
    	for key in list_k:
		os.system(r'cp  ../dataset/CNN_pool/'+data+'/'+key[0] + r' ../dataset/CNN50/train_aug/'+data+'/')
		os.system(r'rm -rf  ../dataset/CNN_pool/'+data+'/'+key[0])


#read data
imgs = {}
labels = {}
data_classes = ["concrete","grass","pave"]
#data = "concrete"
src = '../dataset/CNN_pool/'
#load data
#num_classes =3


model2 = keras.models.load_model('cnn_base_model')

for data in data_classes:
	out_put={}
	AL_select={}
	for i, img in enumerate(os.listdir(src+"/"+data+"/")):
        	if img.startswith('.'): continue
        	if img.startswith('Thumbs'): continue
        	print img
        	print i
        	out_put[i] = []
      		AL_select[i] = []
        	out_put[i].append(img)
        	AL_select[i].append(img)
        	curr = cv2.imread(src+"/"+data+"/"+img)
        	# reshape to be [samples][pixels][width][height]
        	b, g, r = curr[:,:,0], curr[:,:,1], curr[:,:,2]
        	x = np.stack((r, g, b), axis=0) # reorder to rgb
        	if not imgs.get(data):
            		imgs[data] = [x]
        	else:
            		imgs[data].append(x)


#load model
#model2 = keras.models.load_model('cnn_base_model')
	X_test = np.array(imgs[data]).astype('float32')/255.0
	Y_pred_vecs = model2.predict(X_test, verbose=1)

	print(len(Y_pred_vecs))
	for i in range(len(Y_pred_vecs)):
		print(i)
		out_put[i].append(softmax(Y_pred_vecs[i]))
		AL_select[i].append(cross_entroy(softmax(Y_pred_vecs[i])))
	
#init 

	print(out_put)
	print(AL_select)

#	k=Al_query(AL_select,10)
        k=random_query(AL_select,10)

	put_data(data,k)        



#read data
imgs = {}
labels = {}
src = '../dataset/CNN50/'
sets = os.listdir(src)[0:]
for data in sets: # train, val, test
    if data.startswith('.'): continuecd
    print "on {} set".format(data)
    img_types = os.listdir(src+data+"/")[0:]
    num_classes = len(img_types)
    print num_classes
    for label, img_type in enumerate(img_types):
        print label
        if img_type.startswith('.'): continue

        for i, img in enumerate(os.listdir(src+data+"/"+img_type+"/")):
            if img.startswith('.'): continue
            if img.startswith('Thumbs'): continue
            if i % 1000 == 0: print i
            print img
            curr = cv2.imread(src+data+"/"+img_type+"/"+img)
            # reshape to be [samples][pixels][width][height]
            b, g, r = curr[:,:,0], curr[:,:,1], curr[:,:,2]
            x = np.stack((r, g, b), axis=0) # reorder to rgb
            # one hot encode labels
            y = np.zeros(num_classes)
            y[label] = 1.0
            if not imgs.get(data):
                imgs[data] = [x]
            else:
                imgs[data].append(x)
            if not labels.get(data):
                labels[data] = [y]
            else:
                labels[data].append(y)
for set_type, data in imgs.items():
    print(set_type)
    print(np.array(data).shape)
    print(np.array(labels[set_type]).shape)




X_train = np.array(imgs['train_aug']).astype('float32')/255.0
X_val = np.array(imgs['validation']).astype('float32')/255.0
X_test = np.array(imgs['test']).astype('float32')/255.0
Y_train = np.array(labels['train_aug']).astype('float32')
Y_val = np.array(labels['validation']).astype('float32')
Y_test = np.array(labels['test']).astype('float32')

#load model
#model = larger_model2()
# fit over 10 epochs with a batch size of 200.
model2.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=1000, batch_size=200, verbose=2)
model2.save('cnn_base_model')

# Final evaluation of the model
scores = model2.evaluate(X_test, Y_test, verbose=0)
print("CNN cnn_base_model Error: %.2f%%" % (100-scores[1]*100))


#random_query(AL_select,5)

'''
dict1={}
grass_color = [0,255,0]
concrete_color = [160,82,45]
pave_color= [255,165,0]
dict1[0] = grass_color
dict1[1] = concrete_color
dict1[2] = pave_color
img = np.zeros((1000,2000,3),np.uint8)#Éú³ÉÒ»¸ö¿Õ²ÊÉ«Í¼Ïñ
for i in range(len(out_put)):
	str = out_put[i][0]
	print(str)
	str = str.replace('-','.')
	strlist = str.split('.')
	start_x =  ((int)(strlist[0]))*100
	start_y =  ((int)(strlist[1]))*100
	judge = find_max(out_put[i][1])
	print(judge)
	filling_rect(img,start_x,start_y,100,100,dict1[judge])


scipy.misc.imsave('map.jpg', img)	

'''



