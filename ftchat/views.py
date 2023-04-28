import datetime
import json
import random
import uuid

import bcrypt
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_redis import get_redis_connection

from ftchat.models import User

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

    hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    new_user = User(
        user_id=uuid.uuid4(),
        username=username,
        password=hashed_password,
        email=email,
        avatar=avatar,
        created_at=datetime.datetime.now(),
        last_login_at=datetime.datetime.now(),
        sentiment_analysis_enabled=0
    )
    new_user.save()
    return JsonResponse({'result': 'success', 'code': 200, 'message': '用户注册成功'})