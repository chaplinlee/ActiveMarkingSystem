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

def data_set_input(requset):

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
    # TODO:
    # Get value of radio button
    radio_value = request.POST.get("flag")
    # Get path of pushed image
    image_path = request.POST.get("pushing_image").replace('/static','')
    # Edit database
    models.ImgSet.objects.filter(img_name = image_path).update(mark_flag = str(radio_value))


def login(request):
    if request.method == 'GET':
        # data_set_input(request)
        return render(request, "login.html")

    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == 'admin' and password == '123':
            return HttpResponseRedirect(reverse('page_marking'))
        else:

            return HttpResponse('error user!')

def page_marking(request):


    if request.method == 'GET':
        image_push = "/static" + random_image_push()
        return render(request, "page_marking.html", {"image_push": image_push})

    elif request.method == 'POST':
        user_marking(request)
        image_push = "/static" + random_image_push()
        return render(request, "page_marking.html", {"image_push": image_push})