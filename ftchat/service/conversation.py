from ftchat.models import Conversation, Participant, User, Group

def get_conversations(uid):
    conversations = []
    if Participant.objects.filter(user=uid).exists():
        conversation_ids = Participant.objects.filter(user=uid).values_list('conversation', flat=True)
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
                group = Group.objects.get(group_id=group_id)
                _conversation = {
                    'conversation_name': group.group_name,
                    'conversation_avatar': group.avatar,
                    'conversation_id': conversation['id']
                }
                conversations.append(_conversation)
    return conversations