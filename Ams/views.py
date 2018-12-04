from django.shortcuts import render
import sqlite3
import os
from Ams import models
# Create your views here.
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def data_set_input(requset):

    unmarked = -1  # unmarked img flag
    data_set_dir_path = ".\data_set\photo_cam1\\"
    data_set_category = "road_camera"

    # database connect
    conn = sqlite3.connect('.\db.sqlite3')
    c = conn.cursor()

    #clean test data
    delete_sql = """delete from ImgSet"""
    c.execute(delete_sql)

    path_dir = os.listdir(data_set_dir_path)

    for all_dir in path_dir:
        img_name = #real img name
        img_cat = data_set_category
        img_flag = unmarked
        c.execute("insert into ImgSet (img_name,img_cat,img_flag) values (?, ?, ?)",
                  (img_name, img_cat, img_flag))
        conn.commit()
    conn.close()


def login(request):
    if request.method == 'GET':
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
    # TODO

    return render(request, "page_marking.html")