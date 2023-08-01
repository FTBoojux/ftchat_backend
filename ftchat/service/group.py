from django.http import JsonResponse
from ftchat.models import GroupJoinRequest

def save_group_Join_request(uid,group_id,message):
    # 检查是否重复请求
    if GroupJoinRequest.objects.filter(group=group_id,user=uid).exists():
        return JsonResponse({'result':'fail','message':'已经申请过了','code':200,'data':''})
    GroupJoinRequest.objects.create(
        group=group_id,
        user=uid,
        status='pending',
        message=message
    )
    return JsonResponse({'result':'success','message':'申请成功','code':200,'data':''})