import json
import random

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django_redis import get_redis_connection

from ftchat_backend.base_result import success, fail


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
    redis_conn = get_redis_connection('default')
    redis_conn.setex(f'verification_code_{email}', 600, verification_code)


@require_POST
@csrf_exempt
def request_verification_code(request):
    data = json.load(request)
    email = data.get('email','')
    if not email:
        return JsonResponse({'result': 'error', 'message': 'Email address is required'})
    try:
        send_verification_code(email)
        return JsonResponse({'result': 'success', 'message': '验证码已发送，请查收'})
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': '发送验证码失败，请重试'})