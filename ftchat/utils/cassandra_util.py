from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid
from datetime import datetime
from cassandra.query import SimpleStatement
import base64
from ftchat.applicationConf import cassandra_host, cassandra_port, cassandra_username, cassandra_password

auth_provider = PlainTextAuthProvider(
        username=cassandra_username, password=cassandra_password)
cluster = Cluster(contact_points=[cassandra_host], auth_provider=auth_provider)
session = cluster.connect()
session.execute("USE ftchat;")

# 现在你可以使用 session 对象来执行 Cassandra CQL 查询



def save_message(content, sender, receiver, conversation_id):
    # 创建一个唯一的message_id和时间戳
    message_id = str(uuid.uuid4())
    # 把sender和receiver的顺序固定下来，这样就可以保证每个会话的唯一性
    # 给sender和receiver排序，然后把它们拼接起来作为srkey
    if sender > receiver:
        srkey = receiver + sender
    else:
        srkey = sender+receiver
    send_at = datetime.now()
    read = False  # 假设消息刚被创建时尚未读
    sentiment_analysis_result = None  # 根据你的需要填写情感分析结果
    
    # 插入新的记录
    session.execute(
        """
        INSERT INTO gpt_message (message_id, conversation_id, srkey, sender, receiver, content_type, content, send_at, read, sentiment_analysis_result)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (message_id, conversation_id, srkey, sender, receiver, 1, content, send_at, read, sentiment_analysis_result)
    )

def get_message_list(sender, receiver, conversation_id, page_size=10, paging_state=None):
    if sender > receiver:
        srkey = receiver + sender
    else:
        srkey = sender + receiver

    statement = SimpleStatement(
        """
        SELECT message_id, sender , content
        FROM gpt_message
        WHERE conversation_id = %s AND srkey = %s
        ORDER BY send_at DESC
        """,
        fetch_size=page_size
    )

    result_set = session.execute(statement, (conversation_id, srkey), paging_state=paging_state)

    rows = result_set.current_rows
    next_paging_state = result_set.paging_state

    return rows, next_paging_state

def save_conversation_message(conversation_id,uid,message,is_group_chat,message_type=1):
    message_id = str(uuid.uuid4())
    timestamp = datetime.now()
    session.execute(
        """
        INSERT INTO chat_message(conversation_id, message_id,sender_id,timestamp,message_type,content,is_group_chat,sentiment_analysis_result)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (conversation_id,message_id,uid,timestamp,message_type,message,is_group_chat,"")
    )
    return message_id,timestamp

def get_conversation_message_list(conversation_id, uid, page_size=10, paging_state=None):
    statement = SimpleStatement(
        """
        SELECT conversation_id, content, message_id, message_type, sender_id, timestamp, sentiment_analysis_result
        FROM chat_message
        WHERE conversation_id = %s
        ORDER BY timestamp DESC
        """,
        fetch_size=page_size
    )

    result_set = session.execute(statement, (conversation_id,), paging_state=paging_state)

    rows = result_set.current_rows
    next_paging_state = result_set.paging_state
    if next_paging_state is not None:
        next_paging_state = base64.b64encode(next_paging_state).decode()
    return rows[:page_size], next_paging_state

def get_last_message(conversation_id):
    statement = SimpleStatement(
        """
        SELECT conversation_id, content
        FROM chat_message
        WHERE conversation_id = %s
        """
    )
    result_set = session.execute(statement, (conversation_id,))
    rows = result_set.current_rows
    if len(rows) == 0:
        return ""
    return rows[0].content