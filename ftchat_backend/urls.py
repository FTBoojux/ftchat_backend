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
from ftchat.views.account import user as account_views
from ftchat.views.gpt import gpt_views
from ftchat.views.conversation import conversation_views
from ftchat.views.message import message_views
from ftchat.views.group import group_views
from ftchat.views.group import group_members_view as group_members_views
from ftchat.views.attachment import attachment_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/request_verification_code/', views.request_verification_code, name='request_verification_code'),
    path('account/register/',views.register, name='register'),
    path('account/upload_avatar/',views.upload_avatar, name='upload_avatar'),
    path('account/login/',views.login,name='login'),
    path('account/login_inner/',views.login_inner,name='login_inner'),
    path('account/contacts/',account_views.ContactView.as_view(),name='friends'),
    path('account/contacts/<str:user_id>/',account_views.ContactView.as_view(),name='friends'),
    path('account/strangers/',account_views.UserInfoForAddedView.as_view(),name='strangers'),
    path('account/contact_add/',account_views.AddContactView.as_view(),name='add_friend'),
    path('account/logout/',account_views.LogoutView.as_view(),name='logout'),
    path('account/avatar/',account_views.AvatarView.as_view(),name='avatar'),
    path('account/user_info/',account_views.UserInfoForEditView.as_view(),name='user_info'),
    path('gpt/chat/',gpt_views.GptConversation.as_view(),name='chat_gpt'),
    path('gpt/conversation/',gpt_views.ConversationView.as_view(),name='conversation_create'),
    path('message/new_message_num/',message_views.MessageNums.as_view(),name='new_message_num'),
    path('conversations/',conversation_views.ConversationView.as_view(),name='conversations'),
    path('group/',group_views.GroupView.as_view(),name='group'),
    path('groups/<str:group_id>/join_requests/',group_views.GroupJoinRequestView.as_view(),name='group_join_request'),
    path('groups/join_requests/',group_views.GroupJoinRequestView.as_view(),name='group_join_requests'),
    path('search/',account_views.ConversationSearchView.as_view(),name='search'),
    path('groups/<str:group_id>/members/',group_members_views.GroupMembersView.as_view(),name='group_members'),
    path('conversation/<str:conversation_id>/participants/',group_members_views.GroupMembersView.as_view(),name='conversation_participants'),
    path('conversation/<str:conversation_id>/message/',conversation_views.ConversationMessageView.as_view(),name='conversation_message'),
    path('file/attachments/',attachment_views.AttachmentViews.as_view(),name='attachments'),
]
