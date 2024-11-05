from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task
import ftchat.utils.elasticsearch_util as es_util

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ftchat.settings')

app = Celery('ftchat')

app.config_from_object('django.conf:settings', namespace='CELERY')

# 指定并发池类型
app.conf.update(
    worker_pool='threads',  # 或 'threads'
)

# 自动发现任务
app.autodiscover_tasks()

@shared_task
def save_chat_message_to_es(message_id, conversation_id, uid, message, is_group_chat, timestamp, message_type=1):
    es_util.save_conversation_message(message_id, conversation_id, uid, message, is_group_chat, timestamp, message_type)