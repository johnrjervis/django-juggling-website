from django.urls import path
from . import views

app_name = 'dev'
urlpatterns = [
    path('programming/', views.programming, name = 'programming'),
]
