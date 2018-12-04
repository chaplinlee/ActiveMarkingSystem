# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
import os
from Ams import models


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def data_set_input(requset):

    unmarked = '-1'  # unmarked img flag
    data_set_dir_path = '/data_set/photo_cam1/'
    data_set_category = 'road_camera'

    path_dir = os.listdir('./static' + data_set_dir_path)
    for all_dir in path_dir:

        name = data_set_dir_path + os.path.join(all_dir)
        category = data_set_category
        flag = unmarked

        models.ImgSet.objects.create(
            img_name=name,
            img_cat=category,
            mark_flag=flag
        )


def login(request):
    if request.method == 'GET':
        data_set_input(request)
        return render(request, "login.html")

    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == 'admin' and password == 'admin':
            return render(request, "page_marking.html")
        else:
            print('error')
            return render(request, "login.html")


def marking(request):
    # TODO:

    return render(request, "page_marking.html")