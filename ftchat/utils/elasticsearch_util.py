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

def conversation_message_search(conversation_id, keyword, pageNum=1, pageSize=10):
    # 计算起始位置
    from_index = (pageNum - 1) * pageSize

    # 构建查询
    query = {
        "bool": {
            "must": [
                {
                    "term": {
                        "data.conversation_id": conversation_id
                    }
                },
                {
                    "match_phrase": {
                        "data.content": keyword
                    }
                }
            ]
        }
    }
    # 添加高亮设置
    highlight = {
        "pre_tags": ["<em>"],  # 高亮开始标签
        "post_tags": ["</em>"],  # 高亮结束标签
        "fields": {
            "data.content": {}
        }
    }
    # 构建搜索请求体
    search_body = {
        "query": query,
        "from": from_index,
        "size": pageSize,
        "sort": [
            {
                "data.timestamp": {
                    "order": "desc"
                }
            }
        ],
        "highlight": highlight
    }

    # 执行搜索
    response = es_client.search(
        index="chat_message",  # 替换为您的索引名称
        body=search_body
    )

    # 获取结果
    hits = response['hits']['hits']
    total = response['hits']['total']['value']

    # 返回查询结果和总数
    return hits, total