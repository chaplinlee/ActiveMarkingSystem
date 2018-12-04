from django.contrib import admin

# Register your models here.
from Ams import models
admin.site.register(models.ImgSet)
admin.site.register(models.AdminMarker)