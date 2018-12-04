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
    data_set_dir_path = ".\\static\\data_set\\photo_cam1\\"
    data_set_category = "road_camera"

    # # database connect
    # conn = sqlite3.connect('.\db.sqlite3')
    # c = conn.cursor()
    #
    # #clean test data
    # delete_sql = """delete from Ams_imgset"""
    # c.execute(delete_sql)
    #
    # path_dir = os.listdir(data_set_dir_path)
    #
    # for all_dir in path_dir:
    #     # img_main_path = os.path.join(all_dir)
    #     # img_name = data_set_dir_path+img_main_path #real img name
    #     # img_cat = data_set_category
    #     # mark_flag = unmarked
    #     # print('path:'+img_main_path+' name:'+img_name)
    #     # c.execute("insert into Ams_ImgSet (img_name,img_cat,mark_flag) values (?, ?, ?)",
    #     #           (img_name, img_cat, mark_flag))
    #
    #     name = data_set_dir_path + os.path.join(all_dir)
    #     category = data_set_category
    #     flag = unmarked
    #
    #     # print('n:' + img_name + " c:" + img_cat)
    #     c.execute("INSERT INTO Ams_imgset (img_name, img_cat, mark_flag) VALUES (?, ?, ?)",
    #               (name, category, flag))
    #     conn.commit()
    # conn.close()

    path_dir = os.listdir(data_set_dir_path)
    for all_dir in path_dir:

        name = data_set_dir_path + os.path.join(all_dir)
        category = data_set_category
        flag = unmarked

        models.ImgSet.objects.create(
            img_name = name,
            img_cat = category,
            mark_flag = flag
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