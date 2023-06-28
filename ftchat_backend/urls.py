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
from ftchat.views.account import user as account_views
from ftchat.views.gpt import gpt_views
from ftchat.views.message import message_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/request_verification_code/', views.request_verification_code, name='request_verification_code'),
    path('account/register/',views.register, name='register'),
    path('account/upload_avatar/',views.upload_avatar, name='upload_avatar'),
    path('account/login/',views.login,name='login'),
    path('account/friends/',account_views.UserInfoForAddView.as_view(),name='friends'),
    path('account/strangers/',account_views.UserInfoForAddedView.as_view(),name='strangers'),
    path('account/contact/',account_views.AddContactView.as_view(),name='add_friend'),
    path('account/logout/',account_views.LogoutView.as_view(),name='logout'),
    path('account/avatar/',account_views.AvatarView.as_view(),name='avatar'),
    path('account/user_info/',account_views.UserInfoForEditView.as_view(),name='user_info'),
    path('gpt/chat/',gpt_views.GptConversation.as_view(),name='chat_gpt'),
    path('gpt/conversation/',gpt_views.ConversationView.as_view(),name='conversation_create'),
    path('message/new_message_num/',message_views.MessageNums.as_view(),name='new_message_num'),
]
