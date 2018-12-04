from django.db import models

# Create your models here.


# marker model
class AdminMarker(models.Model):
    user_name = models.CharField(max_length=200)
    psd = models.CharField(max_length=200)

# img set model
class ImgSet(models.Model):
    img_name = models.CharField(max_length=200)
    img_cat = models.CharField(max_length=200)  # img category
    mark_flag = models.CharField(max_length=200)