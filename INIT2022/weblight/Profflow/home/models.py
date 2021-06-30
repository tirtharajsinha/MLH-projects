from django.db import models
from django.utils.regex_helper import contains
import datetime
# Create your models here.

class userdetail(models.Model):
    
    username=models.CharField(max_length=112)
    firstname=models.CharField(max_length=112)
    lastname=models.CharField(max_length=112)
    email=models.CharField(max_length=112)
    phone=models.CharField(max_length=12,default="")
    bio=models.TextField()
    pic=models.ImageField(default="",upload_to="profiles")
    website=models.CharField(max_length=112,default="")
    instagram=models.CharField(max_length=112,default="https://instagram.com")
    facebook=models.CharField(max_length=112,default="https://facebook.com")
    twitter=models.CharField(max_length=112,default="https://twitter.com")
    other=models.TextField(default="")
    highlight=models.TextField(default="")
    objects = models.Manager()


    def __str__(self):
        return self.username

 

class analytic(models.Model):
    username=models.CharField(max_length=50)
    total=models.IntegerField(default=0)
    year=models.IntegerField(default=datetime.datetime.now().year)
    month=models.IntegerField(default=datetime.datetime.now().month)
    prev=models.IntegerField(default=0)
    w1=models.IntegerField(default=0)
    w2=models.IntegerField(default=0)
    w3=models.IntegerField(default=0)
    w4=models.IntegerField(default=0)

    def __str__(self):
        return self.username




