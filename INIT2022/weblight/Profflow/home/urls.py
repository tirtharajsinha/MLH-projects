from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('',views.index,name="home"),
    path("user/", views.user,name="home"),
    path('user/login',views.loginuser,name="login"),
    path('user/logout',views.logoutuser,name="logout"),
    path("user/register",views.register,name="register"),
    path("user/deluser",views.del_user,name="del_user"),
    path("user/makeport",views.makeport,name="makeport"),
    path("user/upload",views.makeport,name="makeport"),
    path("<username>",views.portfolio,name="portfolio"),
    path("user/update",views.update,name="update"),
    path("user/search",views.search,name="search"),
    path("user/auto",views.autocomplete,name="autocomplete"),
    path("user/analytics",views.analytics,name="analytics"),
    # path("about",views.about,name="about"),
    # path("services",views.services,name="services"),
    # path("contact",views.contact,name="contact"),
    # path("portfolio",views.portfolio,name="portfolio"),
    
    # path("profile",views.profile,name="profile"),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)