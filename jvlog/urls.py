"""jvlog URL Configuration

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
from django.contrib import admin
from django.urls import include, path
from vlog import urls as vlog_urls
from vlog import views as vlog_views
from dev import urls as dev_urls
from os import environ as os_environ

urlpatterns = [
    path('', vlog_views.index_redirect),
    path(f"{os_environ.get('ADMIN_URL')}/", admin.site.urls),
    path('juggling/', include(vlog_urls)),
    path('dev/', include(dev_urls)),
]
