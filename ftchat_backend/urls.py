"""ftchat_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from ftchat.views import base_views as views 
from ftchat.views import chat_gpt as chat_gpt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/request_verification_code/', views.request_verification_code, name='request_verification_code'),
    path('account/register/',views.register, name='register'),
    path('account/upload_avatar/',views.upload_avatar, name='upload_avatar'),
    path('account/login/',views.login,name='login'),
    path('gpt/chat/',chat_gpt_views.chat_to_gpt,name='chat_gpt'),
]
