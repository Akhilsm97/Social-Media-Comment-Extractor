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
