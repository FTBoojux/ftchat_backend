from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid
from datetime import datetime

from ftchat.applicationConf import cassandra_host, cassandra_port, cassandra_username, cassandra_password

auth_provider = PlainTextAuthProvider(
        username=cassandra_username, password=cassandra_password)
cluster = Cluster(contact_points=[cassandra_host], auth_provider=auth_provider)
session = cluster.connect()
session.execute("USE ftchat;")

# 现在你可以使用 session 对象来执行 Cassandra CQL 查询



def save_message(content, sender, receiver):
    # 创建一个唯一的message_id和时间戳
    message_id = str(uuid.uuid4()) 
    send_at = datetime.now()
    read = False  # 假设消息刚被创建时尚未读
    sentiment_analysis_result = None  # 根据你的需要填写情感分析结果
    
    # 插入新的记录
    session.execute(
        """
        INSERT INTO gpt_message (message_id, sender, receiver, content_type, content, send_at, read, sentiment_analysis_result)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (message_id, sender, receiver, 1, content, send_at, read, sentiment_analysis_result)
    )