# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
import os
from Ams import models
from django.db.models import Q
import random
#
# def data_set_input(requset):
#
#     unmarked = '-1'  # unmarked img flag
#     data_set_dir_path = '/data_set/photo_cam1/'
#     data_set_category = 'road_camera'
#
#     path_dir = os.listdir('./static' + data_set_dir_path)
#     for all_dir in path_dir:
#
#         name = data_set_dir_path + os.path.join(all_dir)
#         category = data_set_category
#
#         flag_tag = unmarked
#         flag_tag_judgement = unmarked
#
#
#         models.ImgSet.objects.create(
#             img_name = name,
#             img_cat = category,
#             mark_flag = flag_tag,
#             img_tag_judgement = flag_tag_judgement
#         )
#
# def data_set_input(img_name, img_cat, mark_flag, img_tag_judgement, table_name):
#
# def data_set_input(request):
#     unmarked = '-1'
#     data_set_dir_path = ''
#     rootdir = '/data_set/'
#
#     dir_list = os.listdir(rootdir)
#     for i in range(0, len(dir_list)):
#         category = dir_list
#         for file in path_file:
#             name =1;
#             flag_tag = unmarked
#             flag_tag_judgement = unmarked
#
#             models.ImgSet.objects.create(
#                         img_name = name,
#                         img_cat = category,
#                         mark_flag = flag_tag,
#                         img_tag_judgement = flag_tag_judgement
#                     )
#

#
#
def random_image_push(self):

    query_array = []
    query_result = models.ImgSet.objects.filter(
        Q(img_cat='road_camera')
        & Q(mark_flag='-1')
    )

    for result in query_result:

        query_array.append(result.img_name)

    random_num =random.randint(0, len(query_array))
    return random_num
    #TODO:
    # get mark from web user_mark = 0 or 1
    # edit query_result[random_num].mark_flag = user_mark
    # contiues


def login(request):
    if request.method == 'GET':
        # data_set_input(request)
        return render(request, "login.html")

    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == 'admin' and password == 'admin':
            random_image_push(request)
            return render(request, "page_marking.html")
        else:
            print('error')
            return render(request, "login.html")


def marking(request):
    # TODO:
    push_img = random_image_push()
    print('1')
    print(push_img)
    if request.method == 'GET':
        push_img = random_image_push()
        print('2')
        print(push_img)
    return render(request, "page_marking.html", {"push_img": push_img})