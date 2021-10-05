from django.db import models

# Create your models here.
class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    post_text = models.CharField(max_length=100)
    post_img = models.CharField(max_length=50)

class Likes(models.Model):
    post_id = models.CharField(max_length=5)
    like_username = models.CharField(max_length=20)

class Comments(models.Model):
    post_id=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    comment=models.CharField(max_length=100)
    DATE=models.CharField(max_length=50)

class Addfriend(models.Model):
    username=models.CharField(max_length=50)
    followingusername=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    notification=models.CharField(max_length=50)

class Admin(models.Model):
    roll=models.CharField(max_length=50)
    username=models.CharField(max_length=50)

class Profilepic(models.Model):
    username=models.CharField(max_length=50)
    profile_pic=models.CharField(max_length=50)





