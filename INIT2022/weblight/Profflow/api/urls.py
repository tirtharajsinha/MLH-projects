from django.contrib import admin
from django.urls import path, include
from api import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('', views.index, name="api"),
    path('dashboard', views.index, name="dashboard"),
    path('console', views.index, name="generateapi"),
    path('scraper=<username>api=<slug:api>query=<user>',
         views.getdata, name="getdata"),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
