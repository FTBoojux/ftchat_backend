from ftchat.models import ContactRequest,GroupJoinRequest,Group,Conversation

def get_message_nums(uid):
    contacts = ContactRequest.objects.filter(receiver=uid,status="pending").count()
    # 查找所有由该用户创建的群聊
    groups = Group.objects.filter(owner=uid)
    # 查找所有由该用户创建的群聊的加群请求
    group_join_requests = GroupJoinRequest.objects.filter(group__in=groups,status="pending").count()    
    return {"contacts":contacts+group_join_requests,"messages":0}