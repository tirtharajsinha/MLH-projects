
from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from home.models import userdetail
from django.forms.models import model_to_dict

from datetime import datetime
# Create your views here.

def index(request):
    
    
    return render(request,"index.html")

def getdata(request,username,api,user):
    try:
        userdata=userdetail.objects.values('username','firstname',"lastname","email","phone","website",
    "instagram","facebook","twitter","other","highlight").get(username=user)
    except:
        userdata={"status_code":404,
                "response":"no username found named : "+user}
    # data=[userdata]
    # print(type(data))
    # return HttpResponse("api is "+api+"<br>user is "+user)
    
    userdata["scraper"]=username
    return JsonResponse(userdata)