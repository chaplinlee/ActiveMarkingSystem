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

    print("Input Road Data Successfully!")


def road_ground_truth_input():

    unmarked = '-1'  # unmarked img flag
    data_set_dir_path = '/data_set/groundtruth/'
    data_set_category = 'ground_truth'

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

    print("Input Ground truth Successfully!")


def helmet_dataset_input():

    unmarked = '-1'  # unmarked img flag
    dataset_dir_path = '/data_set/safetyHelmet/heldatadir/'
    category = 'helmet_data'

    path_dir = os.listdir('./static' + dataset_dir_path)
    for all_dir in path_dir:
        name = os.path.join(all_dir)
        f = open('./static' + dataset_dir_path + name)
        origin_data = f.read()
        f.close()

        data_rows = origin_data.strip().split('\n')
        for data_row in data_rows:
            item = data_row.strip().split(' ')

            # data processing
            if len(item) == 5:
                del item[0]

            x_central = item[0]
            y_central = item[1]
            rect_width = item[2]
            rect_height = item[3]

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
    print("Input Helmet Data Successfully!")

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

def random_ground_image_push():
    query_array = []
    query_result = models.GroundData.objects.filter(mark_flag = '-1')
    for result in query_result:
        query_array.append(result.img_name)
    random_num = random.randint(0, len(query_array))
    return query_array[random_num]

def helmet_image_push():
    query_array = []
    query_result = models.HelmetData.objects.filter(mark_flag = '-1')
    for result in query_result:
        query_array.append(result.file_name)
    random_num = random.randint(0, len(query_array))
    final_query_result = query_array[random_num]

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
    random_num = random.randint(0, len(query_id_array))
    query_data_result = models.HelmetData.objects.filter(
        Q(id=query_id_array[random_num])
    )
    random_num = random.randint(0, len(query_data_result))
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

    return image_rect_data[random_num]

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

def road_marking(request):
    # Get value of radio button
    '''
    unmark -1
    road 1
    pavement 2
    building 3
    tree 4
    road sign 5
    '''

    radio_value = request.POST.get("flag")
    # Get path of pushed image
    image_path = request.POST.get("pushing_image").replace('/static', '')
    # Edit database
    models.ImgSet.objects.filter(img_name=image_path).update(mark_flag=str(radio_value))


def page_road(request):

    if request.method == 'GET':
        image_push = "/static" + random_image_push('ground_truth')
        return render(request, "page_road.html", {"image_push": image_push})

    elif request.method == 'POST':
        road_marking(request)
        image_push = "/static" + random_image_push('ground_truth')
        return render(request, "page_road.html", {"image_push": image_push})

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

# Input data

def page_test(request):
    road_occupation_detection()
    # road_ground_truth_input()
    # road_data_set_input()
    #
    # ground_data_set_input()
    #
    # helmet_dataset_input()
    #
    # path = 'static/data_set/ground_cam/origin_img/'
    # file = os.listdir(path)
    # for filename in file:
    #     name = os.path.join(filename)
    #     image_divide(name)

    return render(request, "page_test.html")

def page_tag_judgement(request):

    return render(request, "page_judgetag.html")

def image_divide(image_name):
    #TODO
    import cv2
    from glob import glob

    origin_image_dir = './static/data_set/ground_cam/origin_img/'
    divided_image_dir = './static/data_set/ground_cam/divided_img/'

    image_path = origin_image_dir + image_name

    img = cv2.imread(image_path)

    width = img.shape[0]
    height = img.shape[1]
    origin_image_name = image_name.split('.')[0]
    origin_image_type = image_name.split('.')[1]

    # img_block_size
    block_size = 256

    for i in range(int(width / block_size)):
        for j in range(int(height / block_size)):
            img_new = img[block_size * i: block_size * (i + 1), block_size * j: block_size * (j + 1), :]

            image_block_name = origin_image_name + '_' + str(i) + '_' + str(j) + '.' + origin_image_type
            image_block_path = divided_image_dir + image_block_name

            cv2.imwrite(image_block_path, img_new)

            print("Now Editing image: " + image_block_name)

    print("Input Ground Data Successfully!")

def ground_data_set_input():
    #TODO:
    block_size = 256
    unmarked = '-1'  # unmarked img flag
    origin_data_set_dir_path = '/data_set/ground_cam/origin_img'
    origin_data_set_category = 'ground_data'

    divided_data_set_dir_path = '/data_set/ground_cam/divided_img'
    query_id_array = []
    origin_path_dir = os.listdir('./static' + origin_data_set_dir_path)
    for all_dir in origin_path_dir:
        name = origin_data_set_dir_path + '/' + os.path.join(all_dir)
        category = origin_data_set_category

        flag_tag = unmarked
        flag_tag_judgement = unmarked

        models.ImgSet.objects.create(
            img_name=name,
            img_cat=category,
            mark_flag=flag_tag,
            img_tag_judgement=flag_tag_judgement
        )
        print("Now input: " + all_dir)

    print("Imgset data input completed")

    divided_path_dir = os.listdir('./static' + divided_data_set_dir_path)
    for all_dir in divided_path_dir:
        image_name = os.path.join(all_dir).split('.')[0]
        image_format = os.path.join(all_dir).split('.')[1]

        origin_img_name = image_name.split('_')[0] + '.' + image_format
        x_block = image_name.split('_')[1]
        y_block = image_name.split('_')[2]

        relative_path = origin_data_set_dir_path + '/' + origin_img_name

        origin_id = models.ImgSet.objects.get(img_name = relative_path).id

        models.GroundData.objects.create(
            img_name = all_dir,
            img_origin_id = origin_id,
            x_block_index = x_block,
            y_block_index = y_block,
            img_size = block_size,
            img_type = unmarked,
            mark_flag = unmarked
        )
        print("Now input: " + image_name + '.' + image_format)
    print("ground data input completed")


def ground_image_marking(request):

    # Get value of radio button
    radio_value = request.POST.get("flag")
    # Get path of pushed image
    image_path = request.POST.get("pushing_image").replace('/static/data_set/ground_cam/divided_img/', '')

    # Edit database
    # 0 for unknown
    # 1 for dirt
    # 2 for Cement
    # 3 for block
    # 4 for grass
    models.GroundData.objects.filter(img_name=image_path).update(img_type=str(radio_value))

    return 0


def page_ground(request):
    if request.method == 'GET':
        image_push = "/static/data_set/ground_cam/divided_img/" + random_ground_image_push()
        return render(request, "page_groundmark.html", {"image_push": image_push})

    elif request.method == 'POST':
        ground_image_marking(request)
        image_push = "/static/data_set/ground_cam/divided_img/" + random_ground_image_push()
        return render(request, "page_groundmark.html", {"image_push": image_push})


def road_occupation_detection():
    import cv2
    import matplotlib.pyplot as plt

    # name = 'static/data_set/div_road/11_14_50_0_0.jpg'
    # img = cv2.imread(name)
    # print(img)

    gtpath = '/data_set/groundtruth/'
    path = 'static/data_set/div_road/'
    file = os.listdir(path)
    for filename in file:

        name = os.path.join(filename)
        # img = cv2.imread(name)

        image_name = name.split('.')[0]
        image_index_x = image_name.split('_')[3]
        image_index_y = image_name.split('_')[4]

        query_index = image_index_x + '_' + image_index_y

        gt = 'static' + gtpath + '_' + query_index

        img = cv2.imread(image_path)
        img_gt = cv2.imread(gt)

        d_value = img - img_gt

        print(d_value)