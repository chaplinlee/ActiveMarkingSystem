# Create your views here.
# encoding=utf8
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
import os
from Ams import models
from django.db.models import Q
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
# main page construction function
def login(request):
    if request.method == 'GET':
        return render(request, "login.html")

    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == 'admin' and password == '123':
            return HttpResponseRedirect(reverse('page_marking'))
        else:

            return HttpResponse('error user!')
def index(request):

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
def helmet_dataset_input():

    unmarked = '-1'  # unmarked img flag
    dataset_dir_path = '/data_set/safetyHelmet/heldatadir/'
    category = 'helmet_data'

    path_dir = os.listdir('./static' + dataset_dir_path)
    for all_dir in path_dir:
        name = os.path.join(all_dir)
        f = open('./static' + dataset_dir_path + name)
        str0 = f.read()
        f.close()
        str1 = str0.strip().split('\n')
        for data_row in str1:
            str2 = data_row.split(' ')
            x_central = str2[0]
            y_central = str2[1]
            rect_width = str2[2]
            rect_height = str2[3]

            models.HelmetData.objects.create(
                file_name=name,
                x_central_point=x_central,
                y_central_point=y_central,
                rect_width=rect_width,
                rect_height=rect_height,
                is_wearing=unmarked,
                mark_flag=unmarked,
                tag_judgement=unmarked
            )
        models.ImgSet.objects.create(
            img_name=dataset_dir_path.replace('heldatadir/', '') + name.replace('txt', 'jpg'),
            img_cat=category,
            mark_flag=unmarked,
            img_tag_judgement=unmarked
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

def helmet_image_push():
    query_array = []
    # query_result = models.ImgSet.objects.filter(
    #     Q(img_cat = image_category)
    #     & Q(mark_flag = '-1')
    # )
    # for result in query_result:
    #     query_array.append(result.img_name)
    # final_query_result = query_array[0].replace('/data_set/safetyHelmet/', '')
    #

    query_result = models.HelmetData.objects.filter(mark_flag = '-1')
    for result in query_result:
        query_array.append(result.file_name)
    final_query_result = query_array[0]
    return final_query_result

def get_helmet_rect(filename):
    image_rect_data = {
        'id':0,
        'file_name': 0,
        'x_central_point': 0,
        'y_central_point': 0,
        'rect_width': 0,
        'rect_height': 0,
        'is_wearing': 0,
        'mark_flag': 0,
        'tag_judgement': 0
    }
    query_id_array = []
    file_data = []

    query_file_result = models.HelmetData.objects.filter(
        Q(file_name = filename)
        & Q(mark_flag = '-1')
    )

    for id_result in query_file_result:
        query_id_array.append(id_result.id)


    query_data_result = models.HelmetData.objects.filter(
        Q(id=query_id_array[0])
    )
    for row in query_data_result:
        file_data.append(row.id)
        file_data.append(row.file_name)
        file_data.append(row.x_central_point)
        file_data.append(row.y_central_point)
        file_data.append(row.rect_width)
        file_data.append(row.rect_height)
        file_data.append(row.is_wearing)
        file_data.append(row.mark_flag)
        file_data.append(row.tag_judgement)

    image_rect_data['id'] = file_data[0]
    image_rect_data['file_name'] = file_data[1]
    image_rect_data['x_central_point'] = file_data[2]
    image_rect_data['y_central_point'] = file_data[3]
    image_rect_data['rect_width'] = file_data[4]
    image_rect_data['rect_height'] = file_data[5]
    image_rect_data['is_wearing'] = file_data[6]
    image_rect_data['mark_flag'] = file_data[7]
    image_rect_data['tag_judgement'] = file_data[8]
    return image_rect_data

def user_marking(request):
    # Get value of radio button
    radio_value = request.POST.get("flag")
    # Get path of pushed image
    image_path = request.POST.get("pushing_image").replace('/static','')
    # Edit database
    models.ImgSet.objects.filter(img_name = image_path).update(mark_flag = str(radio_value))

def helmet_marking(request):
    # Get value of radio button
    radio_value = request.POST.get("flag")

    # Get path of pushed image
    image_id = request.POST.get("img_id_text")
    # image_filename = '/data_set/safetyHelmet/' + request.POST.get("img_filename").replace('txt', 'jpg')

    # Edit database
    # models.ImgSet.objects.filter(img_name=image_filename).update(mark_flag = '1')
    models.HelmetData.objects.filter(id=image_id).update(is_wearing = str(radio_value))
    models.HelmetData.objects.filter(id=image_id).update(mark_flag = '1')


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

        txt_file = helmet_image_push()
        image_name = txt_file.replace('txt','jpg')
        image_push = "/static/data_set/safetyHelmet/" + image_name
        image_rect = get_helmet_rect(txt_file)

        return render(request, "page_helmetjudge.html", {"image_push": image_push, "rect_data": json.dumps(image_rect)})

    elif request.method == 'POST':
        helmet_marking(request)

        txt_file = helmet_image_push()
        image_name = txt_file.replace('txt', 'jpg')
        image_push = "/static/data_set/safetyHelmet/" + image_name
        image_rect = get_helmet_rect(txt_file)

        return render(request, "page_helmetjudge.html", {"image_push": image_push, "rect_data": json.dumps(image_rect)})

def page_test(request):
    # Input data
    #
    # road_data_set_input()
    # ground_data_set_input()

    helmet_dataset_input()
    return  render(request, "page_test.html")

def page_tag_judgement(request):

    return render(request, "page_judgetag.html")

def image_divide():
    #TODO
    return 0

def ground_data_set_input():
    #TODO:

    return 0

def ground_image_push():
    # TODO:

    return 0

def page_ground(request):

    return render(request, "page_groundmark.html")