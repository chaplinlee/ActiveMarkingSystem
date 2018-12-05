# -*- coding: utf-8 -*- 
import cv2
import numpy as np
import os
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
K.set_image_dim_ordering('th')  

# The first hidden layer is a convolutional layer called a Convolution2D. 
# The layer has 32 feature maps, which with the size of 5×5 and a rectifier activation function. 
# This is the input layer, expecting images with the structure outline above [pixels][width][height].
# Next we define a pooling layer that takes the max called MaxPooling2D. 
# It is configured with a pool size of 2×2.
# 
# The next layer is a regularization layer using dropout called Dropout. 
# It is configured to randomly exclude 20% of neurons in the layer in order to reduce overfitting.

# Next is a layer that converts the 2D matrix data to a vector called Flatten. 
# It allows the output to be processed by standard fully connected layers.

# Next a fully connected layer with 128 neurons and rectifier activation function.

# Finally, the output layer has 10 neurons for the 10 classes 
# and a softmax activation function to output probability-like predictions for each class.
# the model is trained using logarithmic loss and the ADAM gradient descent algorithm.


# Convolutional layer with 30 feature maps of size 5×5.
# Pooling layer taking the max over 2*2 patches.
# Convolutional layer with 15 feature maps of size 3×3.
# Pooling layer taking the max over 2*2 patches.
# Dropout layer with a probability of 20%.
# Flatten layer.
# Fully connected layer with 128 neurons and rectifier activation.
# Fully connected layer with 50 neurons and rectifier activation.
# Output layer.

def larger_model():
    # create model
    model = Sequential()
    model.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(15, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def larger_model2():
    model = Sequential()
    model.add(Conv2D(20, (5, 5), input_shape=(3, 64, 64), activation='relu'))
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

#model = keras.models.load_model('cnn_base_model')

#load model
model = larger_model2()
# fit over 10 epochs with a batch size of 200.
model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=1000, batch_size=200, verbose=2)
model.save('cnn_base_model') 

# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("CNN cnn_base_model Error: %.2f%%" % (100-scores[1]*100))

'''
# num_classes = 6
model2 = larger_model2()
# fit over 10 epochs with a batch size of 200.
model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=1500, batch_size=200, verbose=2)
model.save('cnn_base_model_8epoch')

scores = model.evaluate(X_test, Y_test, verbose=2)
print("CNN test error cnn_base_model_8epoch: %.2f%%" % (100-scores[1]*100))

# X_train = np.load("X_train.npy")
# X_val = np.load("X_val.npy")
# X_test = np.load("X_test.npy")
# Y_train = np.load("Y_train.npy")
# Y_val = np.load("Y_val.npy")
# Y_test = np.load("Y_test.npy")
model = keras.models.load_model('cnn_base_model')
# model2 = keras.models.load_model('cnn_base_model_8epoch')
print(X_test.shape)
print(X_test[0].shape)

Y_pred_vecs = model.predict(X_test, verbose=1)
# np.save('pred_Ytest_model10', Y_pred_vecs)
print Y_pred_vecs

Y_pred_vecs_val = model.predict(X_val, verbose=1)
# np.save('pred_Yval_model10', Y_pred_vecs_val)
Y_pred_vecs_train = model.predict(X_train, verbose=1)
# np.save('pred_Ytrain_model10', Y_pred_vecs_train)

print Y_pred_vecs.shape

#Y_pred0 = np.apply_along_axis(np.argmax, 1, np.load('pred_Ytest_model.npy'))
Y_pred = np.apply_along_axis(np.argmax, 1, Y_pred_vecs)
Y_true = np.apply_along_axis(np.argmax, 1, Y_test)
# print Y_pred.shape
# print Y_true.shape
# print Y_pred0
# print Y_pred
# print Y_true

Y_pred_val = np.apply_along_axis(np.argmax, 1, Y_pred_vecs_val)
Y_true_val = np.apply_along_axis(np.argmax, 1, Y_val)
# print Y_pred_val
Y_pred_train = np.apply_along_axis(np.argmax, 1, Y_pred_vecs_train)
Y_true_train = np.apply_along_axis(np.argmax, 1, Y_train)

'''
'''
model2

Y_pred_vecs2 = model2.predict(X_test, verbose=1)
Y_pred_vecs_val2 = model2.predict(X_val, verbose=1)
Y_pred_vecs_train2 = model2.predict(X_train, verbose=1)


Y_pred2 = np.apply_along_axis(np.argmax, 1, Y_pred_vecs2)
Y_pred_val2 = np.apply_along_axis(np.argmax, 1, Y_pred_vecs_val2)
Y_pred_train2 = np.apply_along_axis(np.argmax, 1, Y_pred_vecs_train2)
'''
'''
from sklearn.metrics import precision_recall_fscore_support
#scores = precision_recall_fscore_support(Y_true, Y_pred)
#scores = precision_recall_fscore_support(Y_true_val, Y_pred_val)
scores = precision_recall_fscore_support(Y_true_train, Y_pred_train)
print scores[0] #precision
print scores[1] #recall  
print scores[2] #f1
print scores[3] #support, number of occurrences of each label in y_true


counts_pred1 = []
for i in set(Y_pred):
    counts_pred1.append(np.count_nonzero(Y_pred==i))
print(counts_pred1)
Y_pred_enc = np.zeros((len(Y_pred_vecs), 6))
Y_pred_enc[np.arange(len(Y_pred_vecs)), Y_pred] = 1 
print Y_pred_enc

counts_pred = np.apply_along_axis(sum, 0, Y_pred_enc)
counts = np.apply_along_axis(sum, 0, Y_test)
print counts_pred
print counts

conf = confusion_matrix(Y_true, Y_pred)
print conf
conf_val = confusion_matrix(Y_true_val, Y_pred_val)
print conf_val
conf_train = confusion_matrix(Y_true_train, Y_pred_train)
print conf_train
conf2 = confusion_matrix(Y_true, Y_pred2)
print conf2
conf_val2 = confusion_matrix(Y_true_val, Y_pred_val2)
print conf_val2
conf_train2 = confusion_matrix(Y_true_train, Y_pred_train2)
print conf_train2

cm = conf_train # change
normalize = False
if normalize:
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] 
labels=["grass", "concrete", "pave"]
fig = plt.figure(figsize = (10,7))
ax = fig.add_subplot(111)
cax = ax.matshow(cm) 
plt.title('Confusion matrix (Train)') # change
fig.colorbar(cax)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
fmt = '.2f' if normalize else 'd'
for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, format(cm[i, j], fmt),
             horizontalalignment="center", color="white")
plt.xlabel('Predicted')
plt.ylabel('True')
plt.savefig('conf model10 train') # change
'''
