import datetime
import json
import os.path
import random
from typing import Optional
import uuid

import bcrypt
import jwt
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_redis import get_redis_connection
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import binascii

from ftchat.applicationConf import jwt_security_key
from ftchat.applicationConf import ftchat_iv
from ftchat.applicationConf import ftchat_key
from ftchat.utils.minio_utils import upload_file_to_minio
from ftchat.models import User
import ftchat.utils.redis_utils as redis_utils
redis_conn = get_redis_connection('default')



# Create your views here.
def send_verification_code(email):
    verification_code = ''.join([
        str(random.randint(0, 9))
        for _ in range(6)
    ])
    send_mail(
        '您的注册验证码',
        f'您的注册验证码为：{verification_code}',
        '1647284718@qq.com',
        [email],
        fail_silently=False
    )
    redis_conn.setex(f'verification_code_{email}', 600, verification_code)


def _validate_email_and_password(email, password) -> Optional[User]:
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return None
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), user.salt.encode('utf-8')).decode('utf-8')
    if user.password != hashed_password:
        return None
    else:
        return user

def hex_to_bytes(hex_string):
    return binascii.unhexlify(hex_string)

def base64_to_bytes(base64_string):
    return base64.b64decode(base64_string)

def decrypt(encrypted_data):
    cipher = AES.new(ftchat_key, AES.MODE_CBC, ftchat_iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode("utf-8")

@require_POST
@csrf_exempt
def request_verification_code(request):
    data = json.load(request)
    email = data.get('email', '')
    if not email:
        return JsonResponse({'result': 'error', 'message': 'Email address is required', 'code': 200})
    try:
        send_verification_code(email)
        return JsonResponse({'result': 'success', 'message': '验证码已发送，请查收', 'code': 200})
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': '发送验证码失败，请重试', 'code': 200})


@require_POST
@csrf_exempt
def register(request):
    data = json.load(request)
    username: str = data.get('username', '').strip()
    email: str = data.get('email', '').strip()
    password: str = data.get('password', '').strip()
    verify_code: str = data.get('verify_code', '').strip()
    avatar: str = data.get('avatar', '').strip()

    if not username or not email or not password:
        return JsonResponse({'result': 'fail', 'code': '200', 'message': '用户名、邮箱、密码不可为空！'})
    stored_verify_code = redis_conn.get(f'verification_code_{email}').decode('utf-8')
    if verify_code != stored_verify_code:
        return JsonResponse({'result': 'fail', 'code': '200', 'message': '验证码错误或已过期！'})
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    new_user = User(
        user_id=str(uuid.uuid4()),
        username=username,
        password=hashed_password,
        email=email,
        avatar=avatar,
        created_at=datetime.datetime.now(),
        last_login_at=datetime.datetime.now(),
        sentiment_analysis_enabled=0,
        salt=salt.decode('utf-8')
    )
    new_user.save()
    return JsonResponse({'result': 'success', 'code': 200, 'message': '用户注册成功'})


@require_POST
@csrf_exempt
def upload_avatar(request):
    upload_file = request.FILES['avatar']
    if upload_file.size > 4 * 1024 * 1024:
        return JsonResponse({'result': 'fail', 'code': 400, 'message': '头像文件必须在4MB以内！'})

    try:
        Image.open(upload_file)
    except IOError:
        return JsonResponse({'result': 'error', 'code': 400, 'message': '非图片格式文件！'})

    file_extension = os.path.splitext(upload_file.name)[1]
    file_name = f'{str(uuid.uuid4())}{file_extension}'
    file_path = f'avatar/{file_name}'

    minio_url = upload_file_to_minio('ftchat-avatar', file_name, upload_file, upload_file.content_type)
    print(upload_file.content_type)
    return JsonResponse({'result': 'success', 'code': 200, 'message': 'success!', 'data': minio_url})


@require_POST
@csrf_exempt
def login(request):
    data = json.load(request)
    email: str = data.get('email')
    password: str = data.get('password')
    password = decrypt(base64_to_bytes(password))
    user = _validate_email_and_password(email, password)
    if user is not None:
        payload = {
            'user_id': str(user.user_id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }
        access_token = jwt.encode(payload,jwt_security_key,algorithm='HS256')
        redis_utils.token_add(str(user.user_id), access_token)
        response_data = {
            'result': 'success',
            'code': 200,
            'message': '登录成功',
            'data': {
                'access_token': access_token,
            }
        }
        return JsonResponse(response_data)
    else:
        # 邮箱或密码错误
        response_data = {
            'result': 'error',
            'code': 400,
            'message': '邮箱或密码错误'
        }
        return JsonResponse(response_data)

@require_POST
@csrf_exempt
def login_inner(request):

    # 限制内部调用：获取请求地址
    ip = request.META.get('REMOTE_ADDR')
    print("内部登录请求IP地址：", ip)

    data = json.load(request)
    email: str = data.get('email')
    password: str = data.get('password')
    user = _validate_email_and_password(email, password)
    if user is not None:
        payload = {
            'user_id': str(user.user_id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }
        access_token = jwt.encode(payload,jwt_security_key,algorithm='HS256')
        redis_utils.token_add(str(user.user_id), access_token)
        response_data = {
            'result': 'success',
            'code': 200,
            'message': '登录成功',
            'data': {
                'access_token': access_token,
            }
        }
        return JsonResponse(response_data)
    else:
        # 邮箱或密码错误
        response_data = {
            'result': 'error',
            'code': 400,
            'message': '邮箱或密码错误'
        }
        return JsonResponse(response_data)