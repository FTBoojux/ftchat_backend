from ftchat.models import User
from ftchat.models import Contact
from ftchat.models import ContactRequest
import ftchat.utils.redis_utils as redis_utils

from django.db.models import Q
from django.db import connection

def search_contact(user_id,keyword):
    # friend_ids = Contact.objects.filter(user=user_id).values_list('friend', flat=True)
    # users = User.objects.filter(
    #     Q(user_id__in=friend_ids) &
    #     Q(username__icontains=keyword)
    # ).values('user_id', 'username', 'avatar', 'bio')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ftchat_user.username AS username, ftchat_user.user_id AS user_id, ftchat_user.avatar AS avatar, ftchat_user.bio AS bio 
            FROM ftchat_user 
            INNER JOIN ftchat_contact ON ftchat_contact.friend = ftchat_user.user_id
            AND ftchat_contact.user = %s 
            WHERE user_id != %s 
            AND user_id != 1
            AND username LIKE %s
        """, [user_id, user_id, '%' + keyword + '%'])
        rows = cursor.fetchall()
    # 获取查询结果的列名
    column_names = [col[0] for col in cursor.description]
    # 把查询结果转换成字典形式
    results = [dict(zip(column_names, row)) for row in rows]
    return results

def search_stranger(user_id,keyword):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ftchat_user.username AS username, ftchat_user.user_id AS user_id, ftchat_user.avatar AS avatar, ftchat_user.bio AS bio 
            FROM ftchat_user 
            LEFT JOIN ftchat_contact ON ftchat_contact.friend = ftchat_user.user_id
            AND ftchat_contact.user != %s
            WHERE 
            user_id != %s
            AND user_id != 1
            AND username LIKE %s
        """, [user_id, user_id, '%' + keyword + '%'])
        rows = cursor.fetchall()
    column_names = [col[0] for col in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]
    return results

def add_contact(uid, target, message):
    if Contact.objects.filter(user=uid, friend=target).exists():
        return False,"已经是好友!"
    ContactRequest.objects.create(
        requester=uid,
        receiver=target,
        message=message
    )
    return True,"已发送申请!"

def logout(uid,token):
    if User.objects.filter(user_id=uid).exists():
        redis_utils.token_delete(uid,token)
    return "已登出!"

def get_avatar(uid):
    if User.objects.filter(user_id=uid).exists():
        return User.objects.filter(user_id=uid).values('avatar')[0]['avatar']
    else:
        return None

def save_contact_request(uid, target, message):
    if ContactRequest.objects.filter(requester=uid, receiver=target).exists():
        return False
    else:
        ContactRequest.objects.create(
            requester=uid,
            receiver=target,
            message=message
        )
        return True
    
def get_user_info(uid):
    if User.objects.filter(user_id=uid).exists():
        return User.objects.filter(user_id=uid).values('username', 'avatar', 'bio', 'sentiment_analysis_enabled')[0]
    else:
        return None
    
def update_user_info(uid,username,bio,avatar,sentiment_analysis_enabled):
    if User.objects.filter(user_id=uid).exists():
        User.objects.filter(user_id=uid).update(
            username=username,
            bio=bio,
            avatar=avatar,
            sentiment_analysis_enabled=sentiment_analysis_enabled
        )
        return True
    else:
        return False
    
def get_contact_requests(uid):
    if ContactRequest.objects.filter(receiver=uid).exists():
        return list(ContactRequest.objects.filter(receiver=uid).values('requester', 'message', 'timestamp', 'status').order_by('timestamp')) 
    else:
        return []