# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
import os
from Ams import models
from django.db.models import Q
import random
from django.http import HttpResponseRedirect
from django.urls import reverse


def login(request):
    if request.method == 'GET':
        # Input data

        # road_data_set_input()
        # ground_data_set_input()

        return render(request, "login.html")

    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == 'admin' and password == '123':
            return HttpResponseRedirect(reverse('page_marking'))
        else:

            return HttpResponse('error user!')
def index():
    return render(request, "index.html")

def main_page():
    return render(request, "Main_page.html")

# import matplotlib

# matplotlib.use('Agg')
# import cv2
# import numpy as np
# import os
# import matplotlib
# import matplotlib.pyplot as plt
# import itertools
# from sklearn.metrics import confusion_matrix
# from theano import ifelse
# import keras
# from keras.datasets import mnist
# from keras.models import Sequential
# from keras.models import load_model
# from keras.layers import Dense
# from keras.layers import Dropout
# from keras.layers import Flatten
# from keras.layers import Conv2D
# from keras.layers import MaxPooling2D
# from keras.utils import np_utils
# from keras import backend as K
# from keras import regularizers
#
# import scipy.misc
#
# K.set_image_dim_ordering('th')
#
# def larger_model2():
#     model = Sequential()
#     model.add(Conv2D(20, (5, 5), input_shape=(3, 100, 100), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Conv2D(11, (3, 3), activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2)))
#     model.add(Dropout(0.5))
#     model.add(Flatten())
#     model.add(Dense(64, activation='relu'))
#     model.add(Dense(30, activation='relu'))
#     model.add(Dense(num_classes, activation='softmax'))
#     model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
#     return model
#
#
# def softmax(x):
#     return np.exp(x) / np.sum(np.exp(x), axis=0)
#
#
# def filling_rect(img, start_x, start_y, col, row, color):
#     for i in range(col):
#         for j in range(row):
#             img[i + start_x][j + start_y] = color
#
#
# def find_max(list):
#     index = 0
#     max = list[0]
#     for i in range(len(list)):
#         if list[i] > max:
#             index = i
#             max = list[i]
#     return (index)
#
#
# def confirm_species(list):
#     index = 0

def road_data_set_input():

    unmarked = '-1'  # unmarked img flag
    data_set_dir_path = '/data_set/road_cam/'
    data_set_category = 'road_camera'

    path_dir = os.listdir('./static' + data_set_dir_path)
    for all_dir in path_dir:

        name = data_set_dir_path + os.path.join(all_dir)
        category = data_set_category

        flag_tag = unmarked
        flag_tag_judgement = unmarked

        models.ImgSet.objects.create(
            img_name = name,
            img_cat = category,
            mark_flag = flag_tag,
            img_tag_judgement = flag_tag_judgement
        )

def ground_data_set_input():
    #TODO:
    # load data
    # path = "../hu_test/CNNdatas/test/concrete/11.jpg"
    # path = "/static/ground_cam/origin_img/origin_img_00.jpeg"
    # num_classes = 2
    # curr = cv2.imread(path)
    # # temp_image = curr[0:2000,2400:4000]
    # plt.imshow(curr)
    # plt.show()
    # # scipy.misc.imsave('map_real.jpg', temp_image)
    # width = curr.shape[1]
    # height = curr.shape[0]
    # data = "cnn_data"
    # imgs = {}
    # # reshape to be [samples][pixels][width][height]
    #
    # # load model
    # model2 = keras.models.load_model('cnn_base_model')
    #
    # # init
    # size = 100
    # width = size * (width / size)
    # height = size * (height / size)
    # dict1 = {}
    # grass_color = [0, 255, 0]
    # concrete_color = [160, 82, 45]
    # pave_color = [255, 165, 0]
    # unknown_color = [255, 255, 255]
    #
    # dict1[0] = grass_color
    # dict1[1] = concrete_color
    # dict1[2] = pave_color
    # dict1[3] = unknown_color
    #
    # img = np.zeros((height, width, 3), np.uint8)
    #
    # for i in range(height / size):
    #     for j in range(width / size):
    #         X_test = curr[i * size:i * size + size, j * size:j * size + size]
    #         b, g, r = X_test[:, :, 0], X_test[:, :, 1], X_test[:, :, 2]
    #         x = np.stack((r, g, b), axis=0)  # reorder to rgb
    #         imgs[data] = [x]
    #         X_tmp = np.array(imgs['cnn_data']).astype('float32') / 255.0
    #         Y_pred_vecs = model2.predict(X_tmp, verbose=1)
    #         print(Y_pred_vecs[0])
    #         judge = find_max(Y_pred_vecs[0])
    #         print(judge)
    #         filling_rect(img, i * size, j * size, size, size, dict1[judge])
    #
    # scipy.misc.imsave('map_gen.jpg', img)

    return 0

def ground_image_push():
    # TODO:

    return 0

def random_image_push():
    query_array = []
    query_result = models.ImgSet.objects.filter(
        Q(img_cat='road_camera')
        & Q(mark_flag='-1')
    )
    for result in query_result:
        query_array.append(result.img_name)
    random_num = random.randint(0, len(query_array))
    return query_array[random_num]

def user_marking(request):
    # Get value of radio button
    radio_value = request.POST.get("flag")
    # Get path of pushed image
    image_path = request.POST.get("pushing_image").replace('/static','')
    # Edit database
    models.ImgSet.objects.filter(img_name = image_path).update(mark_flag = str(radio_value))



def page_marking(request):

    if request.method == 'GET':
        image_push = "/static" + random_image_push()
        return render(request, "page_marking.html", {"image_push": image_push})

    elif request.method == 'POST':
        user_marking(request)
        image_push = "/static" + random_image_push()
        return render(request, "page_marking.html", {"image_push": image_push})

def page_tag_judgement(request):

    return render(request, "page_judgetag.html")

def image_divide():
    import cv2

    img = cv2.imread("1.JPG")
    print(img.shape)
    for i in range(25):
        for j in range(46):
            p1 = i * 100;
            q1 = j * 100;
            p2 = p1 + 100;
            q2 = q1 + 100;

            cropped = img[p1:p2, q1:q2]  # 裁剪坐标为[y0:y1, x0:x1]
            cv2.imwrite('xpicture/' + str(i) + '_' + str(j) + '.jpg', cropped)