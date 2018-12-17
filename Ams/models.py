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