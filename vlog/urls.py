"""vlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
from . import views

app_name = 'vlog'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('videos/', views.videos_list, name = 'videos'),
    path('videos/<int:jugglingvideo_id>/', views.video_detail, name = 'detail'),
    path('videos/<int:jugglingvideo_id>/add_comment', views.add_comment, name = 'add_comment'),
    path('learn/', views.learn, name = 'learn'),
    path('about/', views.about, name = 'about'),
    path('about/thanks/', views.thanks, name = 'thanks'),
    path('about/history/', views.history, name = 'history'),
]
