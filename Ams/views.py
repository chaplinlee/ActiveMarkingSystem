# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
import os
from Ams import models
from django.db.models import Q
import random


def data_set_input(requset):

    unmarked = '-1'  # unmarked img flag
    data_set_dir_path = '/data_set/photo_cam1/'
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

def random_image_push(request):
    query_array = []
    query_result = models.ImgSet.objects.filter(
        Q(img_cat='road_camera')
        & Q(mark_flag='-1')
    )
    for result in query_result:
        query_array.append(result.img_name)
    random_num = random.randint(0, len(query_array))
    # print(query_array[random_num])
    return query_array[random_num]

def marking(request):
    # TODO:

    if request.method == 'POST':
        # get value of radio button
        radio_value = request.POST.get("flag")
        print(radio_value)
        # get path of picture
        image_path = request.POST.get("image")
        print(image_path)
        # edit mark flag of ImgSet table
        models.ImgSet.object.filter(
            Q(img_name = 'image_path').edit(mark_flag).to(radio_value)
        )
        # repush image
        random_image_push(request)
        # return render(request, "page_marking.html", {})

def login(request):
    if request.method == 'GET':
        # data_set_input(request)
        return render(request, "login.html")

    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == 'admin' and password == 'admin':
            return render(request, "page_marking.html")
        else:
            return render(request, "login.html", {"message": "Wrong password or username!"})

def page_marking(request):

    image_push = ''

    if request.method == 'GET':
        image_push = random_image_push(request)
    else:
        marking(request)
    return render(request, "page_marking.html", {"image_push": image_push})

