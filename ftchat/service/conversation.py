from ftchat.models import Conversation, Participant, User, Group, GroupMember
from ftchat.utils import cassandra_util
from django.http import JsonResponse
from django.utils import timezone
from ftchat.service import account as account_service
import datetime

def get_conversations(uid):
    conversations = []
    conversation_ids = Participant.objects.filter(user=uid).values_list('conversation', flat=True)

    if conversation_ids:
        _conversations = Conversation.objects.filter(id__in=conversation_ids).order_by('-last_message_at').values('id', 'type', 'group', 'last_message_at')
        # for conversation_id in Participant.objects.filter(user=uid).values_list('conversation', flat=True):
        for conversation in _conversations:
            # conversation = Conversation.objects.get(id=conversation_id)
            if conversation['type'] == 'P':
                # 如果是私人会话，查询对方的信息
                participants = Participant.objects.filter(conversation=conversation['id']).exclude(user=uid).first()
                if participants:
                    contact = User.objects.filter(user_id=participants.user).values('username', 'avatar', 'bio', 'sentiment_analysis_enabled')[0]
                    _conversation = {
                        'conversation_name': contact['username'],
                        'conversation_avatar': contact['avatar'],
                        'conversation_id': conversation['id']
                    }
                    conversations.append(_conversation)
            else:
                # 如果是群聊，查询群聊的信息
                group_id = conversation['group']
                if GroupMember.objects.filter(group=group_id, user=uid).exists():
                    group = Group.objects.get(group_id=group_id)
                    _conversation = {
                        'conversation_name': group.group_name,
                        'conversation_avatar': group.avatar,
                        'conversation_id': conversation['id']
                    }
                    conversations.append(_conversation)
    return conversations

def check_conversation_permission(uid,conversation_id):
    # 检查用户会话权限
    conversation = Conversation.objects.get(id=conversation_id)
    if conversation.type == 'P':
        # 对于私人会话，检查用户是否在会话中
        if not Participant.objects.filter(conversation=conversation_id, user=uid).exists():
            return False
    elif conversation.type == 'G':
        # 对于群聊，检查用户是否在群聊中
        if not GroupMember.objects.filter(group=conversation.group, user=uid).exists():
            return False
    return True

def save_message(uid,conversation_id,message):
    # 检查用户会话权限
    conversation = Conversation.objects.get(id=conversation_id)
    if not check_conversation_permission(uid,conversation_id):
        return JsonResponse({'result':'fail','message':'用户没有会话权限','code':403,'data':''})
    Conversation.objects.filter(id=conversation_id).update(last_message_at=timezone.now())
    message_id,timestamp = cassandra_util.save_conversation_message(conversation_id,uid,message,conversation.type=='G')
    # 构建返回的消息
    message = {
        'conversation_id':conversation_id,
        'content':message,
        'message_id':message_id,
        'message_type':1,
        'sender':account_service.get_user_info(uid),
        'timestamp':timestamp,
        'sentiment_analysis_result':'',
        'side':'right'
        }
    return JsonResponse({'result':'success','message':'','code':200,'data':message})

def get_message_list(uid,conversation_id,page_size,paging_state):
    if not check_conversation_permission(uid,conversation_id):
        return JsonResponse({'result':'fail','message':'用户没有会话权限','code':403,'data':''})
    message_list,paging_state = cassandra_util.get_conversation_message_list(conversation_id,uid,page_size,paging_state)
    # for message in message_list:
    #     message.sender = account_service.get_user_info(message.sender_id)
    message_list = [{'conversation_id':message.conversation_id, 
                     'content':message.content,
                     'message_id':message.message_id,
                     'message_type':message.message_type,
                     'sender':account_service.get_user_info(message.sender_id),
                     'timestamp':message.timestamp,
                     'sentiment_analysis_result':message.sentiment_analysis_result,
                     'side':'right' if message.sender_id == uid else 'left'
                     } for message in message_list]
    return JsonResponse({'result':'success','message':'','code':200,'data':{'message_list':message_list,'paging_state':paging_state}})