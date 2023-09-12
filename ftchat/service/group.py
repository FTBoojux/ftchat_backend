from django.http import JsonResponse
from ftchat.models import GroupJoinRequest, Group, User,GroupMember,Conversation,Participant

def save_group_Join_request(uid,group_id,message):
    # 检查是否重复请求
    if GroupJoinRequest.objects.filter(group=group_id,user=uid,status="pending").exists():
        return JsonResponse({'result':'fail','message':'已经申请过了','code':200,'data':''})
    GroupJoinRequest.objects.create(
        group=group_id,
        user=uid,
        status='pending',
        message=message
    )
    return JsonResponse({'result':'success','message':'申请成功','code':200,'data':''})

def get_group_join_requests(uid):
    res = []
    group_ids = Group.objects.filter(owner=uid).values_list('group_id',flat=True)
    group_join_requests = GroupJoinRequest.objects.filter(group__in=group_ids,status="pending")
    for group_join_request in group_join_requests:
        user = User.objects.get(user_id=group_join_request.user)
        group = Group.objects.get(group_id=group_join_request.group)
        res.append({
            "request_id":group_join_request.id,
            "group":{
                "group_id":group.group_id,
                "group_name":group.group_name,
                "group_avatar":group.avatar,
            },
            "requester":{
                "user_id":user.user_id,
                "username":user.username,
                "avatar":user.avatar,
            },
            "message":group_join_request.message,
            "time":group_join_request.created_at,
        })
    return res

def reject_group_join_request(uid,group_id,requester):
    if not Group.objects.filter(group_id=group_id,owner=uid).exists():
        return JsonResponse({'result':'fail','message':'没有权限','code':200,'data':''})
    GroupJoinRequest.objects.filter(group=group_id,user=requester,status='pending').update(status='rejected')
    return JsonResponse({'result':'success','message':'拒绝成功','code':200,'data':''})

def accept_group_join_request(uid,group_id,requester):
    if not Group.objects.filter(group_id=group_id,owner=uid).exists():
        return JsonResponse({'result':'fail','message':'没有权限','code':200,'data':''})
    GroupJoinRequest.objects.filter(group=group_id,user=requester,status='pending').update(status='approved')
    conversation_id = Conversation.objects.get(type='G',group=group_id).id
    Participant.objects.create(
        conversation=conversation_id,
        user=requester
    )
    GroupMember.objects.create(
        group=group_id,
        user=requester,
        nickname=User.objects.get(user_id=requester).username,
        role=3
    )
    return JsonResponse({'result':'success','message':'已通过','code':200,'data':''})

def delete_group_member(uid,group_id):
    # 判断是否是成员本人操作
    if not GroupMember.objects.filter(group=group_id,user=uid).exists():
        # 判断是否是群主操作
        if not Group.objects.filter(group_id=group_id,owner=uid).exists():
            return JsonResponse({'result':'fail','message':'没有权限','code':403,'data':''})        
    GroupMember.objects.filter(group=group_id,user=uid).delete()    
    return JsonResponse({'result':'success','message':'删除成功','code':200,'data':''})

def get_group_members(group_id):
    res = []
    group_members = GroupMember.objects.filter(group=group_id)
    for group_member in group_members:
        user = User.objects.get(user_id=group_member.user)
        res.append({
            "user_id":user.user_id,
            "username":user.username,
            "nickname":group_member.nickname,
            "avatar":user.avatar,
            "role":group_member.role
        })
    return JsonResponse({'result':'success','message':'获取成功','code':200,'data':res})