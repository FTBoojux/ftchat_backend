from ftchat.models import User
from ftchat.models import Contact

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
            WHERE user_id != %s
            AND username LIKE %s
        """, [user_id, user_id, '%' + keyword + '%'])
        rows = cursor.fetchall()
    column_names = [col[0] for col in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]
    return results