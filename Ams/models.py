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
    mark_flag = models.CharField(max_length=200) # image tag
    img_tag_judgement = models.CharField(max_length=200) #image tag judgement

# tagged image set
class TaggedImgSet(models.Model):
    img_name = models.CharField(max_length=200)
    img_cat = models.CharField(max_length=200)  # img category
    mark_flag = models.CharField(max_length=200)  # image tag
    img_tag_judgement = models.CharField(max_length=200)  # image tag judgement

#helmet mark txt file
class HelmetData(models.Model):
    file_name = models.CharField(max_length=100)
    x_central_point = models.FloatField(max_length = 20)
    y_central_point = models.FloatField(max_length = 20)
    rect_width = models.FloatField(max_length = 20)
    rect_height = models.FloatField(max_length = 20)
    is_wearing = models.CharField(max_length=10)
    mark_flag = models.CharField(max_length=10)
    tag_judgement = models.CharField(max_length=10)