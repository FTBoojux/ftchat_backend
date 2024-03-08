import os
import uuid
from django.http import JsonResponse
from ftchat.models import Attachment
import ftchat.utils.minio_utils as minio_utils
from ftchat.views.AuthenticateView import AuthenticateView
from datetime import datetime
import ftchat.utils.jwt_util as jwt_utils
class AttachmentViews(AuthenticateView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        file_origin_name = file.name
        file_type = file.content_type
        file_size = file.size
        if file_size > 500 * 1024 * 1024:
            return JsonResponse({'result': 'fail', 'code': 400, 'message': '文件大小不能超过500MB'})
        # 生成文件存储名 格式为 年份 / 月份 / 日期 +uuid+文件后缀
        file_storage_name = f'{datetime.now().year}/{datetime.now().month}/{datetime.now().day}/{str(uuid.uuid4())}{os.path.splitext(file_origin_name)[1]}'
        # 上传文件到minio
        file_url = minio_utils.upload_file_to_minio('ftchat-attachment', file_storage_name, file, file_type)
        # 保存文件信息到数据库
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(request.META.get('HTTP_AUTHORIZATION')))
        attachment = Attachment.objects.create(
            file_name=file_origin_name,
            file_type=file_type,
            file_size=file_size,
            file_url = file_url,
            uploaded_by = uid
        )
        return JsonResponse({'result': 'success', 'code': 200, 'message': '文件上传成功', 'data': {
            'attachment_id' : attachment.attachment_id,
            'url': file_url,
            'type': file_type,
            'file_name': file_origin_name,
            'file_size': file_size,
        }})