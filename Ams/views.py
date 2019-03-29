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

# main page construction function
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

# data input function
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



def random_image_push(image_category):
    query_array = []
    query_result = models.ImgSet.objects.filter(
        Q(img_cat = image_category)
        & Q(mark_flag = '-1')
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
        image_push = "/static" + random_image_push('road_camera')
        return render(request, "page_marking.html", {"image_push": image_push})

    elif request.method == 'POST':
        user_marking(request)
        image_push = "/static" + random_image_push('road_camera')
        return render(request, "page_marking.html", {"image_push": image_push})


def page_helmet_judge(request):

    if request.method == 'GET':
        image_push = "/static" + random_image_push('helmet_data')
        return render(request, "page_helmetjudge.html", {"image_push": image_push})

    elif request.method == 'POST':
        user_marking(request)
        image_push = "/static" + random_image_push('helmet_data')
        return render(request, "page_helmetjudge.html", {"image_push": image_push})


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


def ground_data_set_input():
    #TODO:

    return 0

def ground_image_push():
    # TODO:

    return 0