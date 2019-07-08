"""ActiveMarkingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Ams import views
from django.conf.urls import url
# from django.views import static
# from django.conf import setting
# from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('marking/', views.page_marking, name='page_marking'),
    path('tagjudgement/', views.page_tag_judgement, name='tag_judgement'),
    path('helmetjudge/', views.page_helmet_judge, name='helmet_judge'),
    path('test/', views.page_test, name='test'),
    path('ground/', views.page_ground, name='ground_judge'),
    path('road/', views.page_road, name='road_mark'),
    # url(r'^static/(?P<path>.*)$', static.serve,
    #     {'document_root':setting.STATIC_ROOT}, name='static'),
    # path("", include(('learning_logs.urls','learning_logs'), namespace='learning_logs')),
    # url(r'^login/', views.login),

    # path('^login/$', views.login, name='login'),
    # url(r'^login/$', views.login, name='login'),
]
