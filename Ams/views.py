from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


def login(request):
    if request.method == 'GET':
        return render(request, "login.html")

    else:
        username = request.POST.get('id_username', '')
        password = request.POST.get('id_password', '')

        if username == 'admin' & password == 'admin':
            return render(request, "page_marking.html")
        else:
            print('error')
            return render(request, "login.html")


def marking(request):
    return render(request, "page_marking.html")