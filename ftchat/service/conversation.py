from ftchat.models import Conversation, Participant, User, Group

def get_conversations(uid):
    conversations = []
    if Participant.objects.filter(user=uid).exists():
        for conversation_id in Participant.objects.filter(user=uid).values_list('conversation', flat=True):
            conversation = Conversation.objects.get(id=conversation_id)
            if conversation.type == 'P':
                # 如果是私人会话，查询对方的信息
                participants = Participant.objects.filter(conversation=conversation_id).exclude(user=uid).first()
                if participants:
                    contact = User.objects.filter(user_id=participants.user).values('username', 'avatar', 'bio', 'sentiment_analysis_enabled')[0]
                    _conversation = {
                        'conversation_name': contact['username'],
                        'conversation_avatar': contact['avatar'],
                        'conversation_id': conversation.id
                    }
                    conversations.append(_conversation)
            else:
                # 如果是群聊，查询群聊的信息
                group_id = conversation.group
                group = Group.objects.get(id=group_id)
                _conversation = {
                    'conversation_name': group.group_name,
                    'conversation_avatar': group.avatar,
                    'conversation_id': conversation.id
                }
                conversations.append(_conversation)
    return conversations