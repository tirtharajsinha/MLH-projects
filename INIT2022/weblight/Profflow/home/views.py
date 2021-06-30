from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from home.models import userdetail,analytic

from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, "index.html")

def user(request):
    if request.user.is_anonymous:
        return redirect("/user/login")

    data = userdetail.objects.all()
    userlist = data.values_list("username")
    myuser = str(request.user)
    userid = -1
    #print(myuser, ".........", type(myuser))
    for i in range(len(userlist)):
        print(userlist[i][0], type(userlist[i][0]))
        if userlist[i][0] == myuser:
            userid = i

            break
       
    if request.method=="POST":
        firstname=request.POST.get("firstname")   
        lastname=request.POST.get("lastname")
        email=request.POST.get("email")
        print(firstname,lastname)
        username=request.user
        user=User.objects.get(username=username)
        print(user.first_name,".........")
        user.first_name=firstname
        user.last_name=lastname
        if user.email =="":
            user.email=email
        user.save()
        
        return redirect("/user/")
    if userid==-1:
        mymsg='start to build your profflow now, check out the link "manage your profflow"'
        messages.add_message(request, messages.INFO,mymsg)
                                    
    return render(request, "user.html")

def search(request):
    if request.method=="POST":
        query=request.POST.get("search")
        # print(query)
        query=query.strip()
        return redirect("/"+query)
    return render(request,"search.html")

def autocomplete(request):
    
    query=request.GET.get('term')
    # print(query,".................1")
    queryset=userdetail.objects.filter(username__icontains=query)
    mylist=[]
    mylist+=[x.username for x in queryset]  
    
    return JsonResponse(mylist,safe=False)


def portfolio(request, username):
    data = userdetail.objects.all()
    userlist = data.values_list("username")
    userid = -1
    
    
    for i in range(len(userlist)):
        # print(userlist[i][0], type(userlist[i][0]))
        if userlist[i][0] == username:
            userid = i
            break
    if userid == -1:
        mymsg='No user named {}.Want to search for user? chech out link below'.format(username)
        messages.add_message(request,messages.INFO,mymsg)
        return render(request,"index.html")
    else:
        userdata = data[userid]
        otherlinks=userdata.other
        otherlinks=otherlinks.replace("\n","")
        alllinks=otherlinks.split("+")
        links=[]
        for li in alllinks:
            link=li.split(":",1)
            links.append([link[0],link[-1]])
        # print(links)
        highlights=userdata.highlight
        highlights=highlights.replace("\n","")
        allhigh=highlights.split("+")
        highlight=[]
        for hi in allhigh:
            high=hi.split(":")
            highlight.append([high[0],high[-1]])
        # print("......>>",type(username))    
        analyticsload(username)


        return render(request,"portfolio.html",{"data":userdata,"otherlinks":links,"highlights":highlight})    


def loginuser(request):
    if request.user.is_anonymous==False:
        return redirect("/user/")
    
    if request.method == "POST":
        username = request.POST.get('username')
        passward = request.POST.get('passward')
        user = authenticate(username=username, password=passward)
        if user is not None:
            login(request, user)
            return redirect("/user/")
        else:
            messages.add_message(request, messages.INFO,
                                 "Wrong authentication details !! Try again.")
            return render(request, "login.html")

    return render(request, "login.html")


def logoutuser(request):
    if request.user.is_anonymous:
        return redirect("/")
    logout(request)
    messages.add_message(request, messages.INFO,"you are logged-out. See you later.")
                                 
    return redirect("/")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        passward = request.POST.get('passward')
        try:
            user = User.objects.get(username=username)
            context = {
                'error': 'The username you entered has already been taken. Please try another username.'}
            return render(request, 'register.html', context)
        except User.DoesNotExist:
            User.objects.create_user(username, email, passward)
            logout(request)
            return redirect("/user/login")

    else:
        return render(request, "register.html")


def del_user(request):
    if request.user.is_anonymous:
        return redirect("/user/login")
    username = request.user.username
    try:
        user = User.objects.get(username=username)
        user.delete()
        logout(request)
        
        data=userdetail.objects.get(username=username)
        data.delete()
        messages.success(request, "The user is deleted. Thank you for be with us. We will miss you.")
        return render(request, 'index.html')
    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")
        return render(request, 'index.html')

    except Exception as e:
        return render(request, 'index.html', {'err': e})

    return redirect('user/index')


def makeport(request):
    if request.user.is_anonymous:
        return redirect("/user/login")
    data = userdetail.objects.all()
    userlist = data.values_list("username")
    myuser = str(request.user)
    userid = -1
    print(myuser, ".........", type(myuser))
    for i in range(len(userlist)):
        print(userlist[i][0], type(userlist[i][0]))
        if userlist[i][0] == myuser:
            userid = i

            break
    if userid == -1:
        if request.method == "POST":
            username = request.user
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            bio = request.POST.get('bio')
            pic = request.FILES['image']
            website = request.POST.get('website')
            instagram = request.POST.get('instagram')
            facebook = request.POST.get('facebook')
            twitter = request.POST.get('twitter')
            other = request.POST.get('other')
            highlight = request.POST.get('highlight')
            details = userdetail(username=username, firstname=firstname, lastname=lastname, email=email, pic=pic, phone=phone,
                             bio=bio, website=website, instagram=instagram, facebook=facebook, twitter=twitter, other=other, highlight=highlight)
            details.save()
            analyticdata=analytic(username=username)
            analyticdata.save()


        print("uploaded sucessesfully")
        return render(request, "data-uploader.html")
    else:
        return redirect("/user/update")


def update(request):
    if request.user.is_anonymous:
        return redirect("/user/login")

    
        
    data = userdetail.objects.all()
    userlist = data.values_list("username")
    myuser = str(request.user)
    userid = -1
    print(myuser, ".........", type(myuser))
    for i in range(len(userlist)):
        # print(userlist[i][0], type(userlist[i][0]))
        if userlist[i][0] == myuser:
            userid = i

            break
    if userid == -1:
        return render(request, "data-uploader.html")
    dataid=data[userid].id
    if request.method == "POST":
            
            
            details = userdetail.objects.get(id=dataid)
            details.firstname = request.POST.get('firstname')
            details.lastname = request.POST.get('lastname')
            details.email = request.POST.get('email')
            details.phone = request.POST.get('phone')
            details.bio = request.POST.get('bio')
            pic_per=True
            try:
                details.pic = request.FILES['image']
            except:
                pic_per=False
                
            
            
            details.website = request.POST.get('website')
            details.instagram = request.POST.get('instagram')
            details.facebook = request.POST.get('facebook')
            details.twitter = request.POST.get('twitter')
            details.other = request.POST.get('other')
            details.highlight = request.POST.get('highlight')
            details.save()
            data=userdetail.objects.all()    
    
    # print("found", userid)
    # print(data[userid].id)
    # print(type(data[userid].id))
    userdata = data[userid]
    return render(request, "update.html", {"data": userdata})

def analytics(request):
    if request.user.is_anonymous:
        return redirect("/user/login")
    data = analytic.objects.all()
    userlist = data.values_list("username")
    username=str(request.user).strip()
    print()
    # print(analytic.objects.get())
    if (username,) not in userlist:
        return render(request, "data-uploader.html")


    analytics=analytic.objects.get(username=request.user)
    try:
        growth=(((analytics.w1 + analytics.w2 + analytics.w3 + analytics.w4) - analytics.prev)/analytics.prev) * 100
    except:
        growth=100
    
    growth=int(growth)
    
    w1=analytics.w1
    if w1==0:
        wp1=0
    else:
        wp1=w1/(analytics.w1 + analytics.w2 + analytics.w3 + analytics.w4)*100
    
    w2=analytics.w2
    if w2==0:
        wp2=0
    else:
        wp2=w2/(analytics.w1 + analytics.w2 + analytics.w3 + analytics.w4)*100

    w3=analytics.w3
    if w3==0:
        wp3=0
    else:
        wp3=w3/(analytics.w1 + analytics.w2 + analytics.w3 + analytics.w4)*100

    w4=analytics.w4
    if w4==0:
        wp4=0
    else:
        wp4=w4/(analytics.w1 + analytics.w2 + analytics.w3 + analytics.w4)*100

    week=[int(wp1),int(wp2),int(wp3),int(wp4)]
    # print("---->>>",week)
    # print(growth)
    
    return render(request,"analytics.html",{"analytic":analytics,"growth":growth,"week":week})

def analyticsload(user):
    # print("//////",user)
    data = analytic.objects.all()
    userlist = data.values_list("username")
    # print(userlist)
    if (user,) in userlist:
        userdata=analytic.objects.get(username=user)
        userdata.total+=1
        if userdata.year!=datetime.now().year:
            userdata.year=datetime.now().year
        if userdata.month!=datetime.now().month:
            userdata.month=datetime.now().month
            userdata.prev=userdata.w1+userdata.w2+userdata.w3+userdata.w4
            userdata.w1=0    
            userdata.w2=0 
            userdata.w3=0 
            userdata.w4=0 
        if datetime.now().day<=7:
            userdata.w1+=1
        elif datetime.now().day<=14:
            userdata.w2+=1
        elif datetime.now().day<=21:
            userdata.w3+=1
        else:
            userdata.w4+=1

        userdata.save()
    
        

