from ftchat.models import Attachment
from django.db import connection

def get_files_list(conversation_id,page_size,page_num):
    with connection.cursor() as cursor:
        cursor.execute("""
            select 
                       ftchat_attachment.attachment_id, 
                       ftchat_attachment.file_name, 
                       ftchat_attachment.file_type, 
                       ftchat_attachment.file_size, 
                       ftchat_attachment.uploaded_at, 
                       ftchat_attachment.file_url,
                       ftchat_user.username as uploaded_by
            from ftchat_attachment 
                       inner join ftchat_user on ftchat_attachment.uploaded_by = ftchat_user.user_id
            where conversation_id = %s
            order by uploaded_at desc
            limit %s offset %s
        """, [conversation_id, page_size, page_size * (page_num - 1)])
        rows = cursor.fetchall()
    # 获取查询结果的列名
    column_names = [col[0] for col in cursor.description]
    # 把查询结果转换成字典形式
    results = [dict(zip(column_names, row)) for row in rows]
    return results