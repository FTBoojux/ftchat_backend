from datetime import datetime,timedelta
import os
from io import BytesIO
import uuid

from minio import Minio, S3Error

from ftchat.applicationConf import minio_endpoint, minio_access_key, minio_secret_key, minio_secure

minio_client = Minio(
    minio_endpoint,
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=minio_secure,
)


def upload_file_to_minio(bucket_name, file_name, in_memory_file,content_type):
    # 将InMemoryUploadedFile对象的文件指针移回到开头
    in_memory_file.seek(0)

    # 使用BytesIO将InMemoryUploadedFile对象的内容读取到内存缓冲区中
    file_data = BytesIO(in_memory_file.read())

    # 使用Minio客户端的put_object()方法将文件上传到Minio服务器
    minio_client.put_object(
        bucket_name,
        file_name,
        file_data,
        length=file_data.getbuffer().nbytes,
        content_type=content_type
    )

    # 构建文件在Minio服务器上的URL
    file_url = f"http://{minio_endpoint}{bucket_name}/{file_name}"

    return file_url

def generate_presigned_url(filename):
    object_name = f'{datetime.now().year}/{datetime.now().month}/{datetime.now().day}/{str(uuid.uuid4())}{os.path.splitext(filename)[1]}'
    presigned_url = minio_client.presigned_put_object('ftchat-attachment', object_name, timedelta(seconds=1000))
    return presigned_url