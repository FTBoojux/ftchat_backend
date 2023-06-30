from ftchat.models import User
from ftchat.models import Contact
from ftchat.models import ContactRequest
import ftchat.utils.redis_utils as redis_utils

from django.db.models import Q
from django.db import connection

def search_contact(user_id,keyword):
    # with connection.cursor() as cursor:
    #     cursor.execute("""
    #         SELECT username, user_id, avatar, bio
    #         FROM ftchat_user 
    #         where user_id in(
	# 			select friend from ftchat_contact where user = %s
    #         ) and user_id != '1' and user_id != %s and username like %s
    #     """, [user_id, user_id, '%' + keyword + '%'])
    #     rows = cursor.fetchall()
    # # 获取查询结果的列名
    # column_names = [col[0] for col in cursor.description]
    # # 把查询结果转换成字典形式
    # results = [dict(zip(column_names, row)) for row in rows]
    # return results
    contact_ids = Contact.objects.filter(user=user_id).values_list('friend', flat=True)
    results = User.objects.filter(Q(user_id__in=contact_ids), ~Q(user_id=user_id), ~Q(user_id=1), username__icontains=keyword).values('username', 'user_id', 'avatar', 'bio')
    return list(results)

def search_stranger(user_id,keyword):
    # with connection.cursor() as cursor:
    #     cursor.execute("""
    #         SELECT username, user_id, avatar, bio
    #         FROM ftchat_user 
    #         where user_id not in(
	# 			select friend from ftchat_contact where user = %s
    #         ) and user_id != '1' and user_id != %s and username like %s
    #     """, [user_id, user_id, '%' + keyword + '%'])
    #     rows = cursor.fetchall()
    # column_names = [col[0] for col in cursor.description]
    # results = [dict(zip(column_names, row)) for row in rows]
    # return results
    contact_ids = Contact.objects.filter(user=user_id).values_list('friend', flat=True)
    results = User.objects.exclude(Q(user_id__in=contact_ids) | Q(user_id=user_id) | Q(user_id=1)).filter(username__icontains=keyword).values('username', 'user_id', 'avatar', 'bio')
    return list(results)

def save_contact_request(uid, target, message):
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
    if ContactRequest.objects.filter(receiver=uid,status="pending").exists():
        return list(ContactRequest.objects.filter(receiver=uid).values('requester', 'message', 'timestamp', 'status').order_by('-timestamp')) 
    else:
        return []
    
def add_contact(uid1,uid2):
    if Contact.objects.filter(user=uid1, friend=uid2).exists():
        return False,"已经是好友!"
    Contact.objects.create(
        user=uid1,
        friend=uid2
    )
    Contact.objects.create(
        user=uid2,
        friend=uid1
    )
    ContactRequest.objects.filter(requester=uid2, receiver=uid1).update(status='accepted')
    return True,"已添加好友!"

def reject_contact_request(uid1,uid2):
    ContactRequest.objects.filter(requester=uid2, receiver=uid1).update(status='rejected')
    return "已拒绝!"

def delete_contact(uid1,uid2):
    Contact.objects.filter(user=uid1, friend=uid2).delete()
    Contact.objects.filter(user=uid2, friend=uid1).delete()
    return "已删除!"