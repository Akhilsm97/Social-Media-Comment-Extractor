from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver

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

class Clusters(models.Model):
    cluster = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)

class ClustersNames(models.Model):
    cluster = models.CharField(max_length=100)

class ThreadModel(models.Model):
 	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userthread')
 	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recievername')

# class Thread(models.Model):
#     user =models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
#     receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
  

class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)



