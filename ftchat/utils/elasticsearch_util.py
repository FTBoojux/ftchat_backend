from ftchat.applicationConf import elastic_host, elastic_port, elastic_username, elastic_password
from elasticsearch import Elasticsearch
from datetime import datetime

es_client = Elasticsearch(
            f"http://{elastic_host}:{elastic_port}",
            basic_auth=(elastic_username, elastic_password),
            verify_certs=False,  # 生产环境建议设置为True
            request_timeout=30
        )

def save_conversation_message(message_id, conversation_id, uid, message, is_group_chat, timestamp, message_type=1):
    data = {
        "conversation_id": conversation_id,
        "timestamp": timestamp,
        "message_id": message_id,
        "content": message,
        "is_group_chat": is_group_chat,
        "message_type": message_type,
        "sender_id": uid,
        "sentiment_analysis_result": ""
    }
    document = {
        'id': message_id,
        'data': data,
        'updated_at': datetime.now()
    }
    es_client.index(index='chat_message', id=message_id, body=document)