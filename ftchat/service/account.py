from ftchat.models import User
from ftchat.models import Contact

from django.db.models import Q

def search_contact(user_id,keyword):
    friend_ids = Contact.objects.filter(user=user_id).values_list('friend', flat=True)
    users = User.objects.filter(
        Q(user_id__in=friend_ids) &
        Q(username__icontains=keyword)
    ).values('user_id', 'username', 'avatar', 'bio')

    return users