# from djongo import models
from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=64)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    avatar = models.CharField(max_length=256)
    bio = models.CharField(max_length=256)
    created_at = models.DateTimeField()
    last_login_at = models.DateTimeField()
    sentiment_analysis_enabled = models.IntegerField()
    salt = models.CharField(max_length=256)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.user_id+','+str(self.sentiment_analysis_enabled)

class Message(models.Model):
    message_id = models.IntegerField(primary_key=True)
    sender = models.IntegerField()
    receiver = models.IntegerField()
    content_type = models.CharField(max_length=50)
    content = models.CharField(max_length=256)
    sent_at = models.DateTimeField()
    read = models.BooleanField()
    sentiment_analysis_result = models.CharField(max_length=256, null=True)


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=64)
    friend = models.CharField(max_length=64)
    remark = models.CharField(max_length=50, null=True)
    group = models.CharField(max_length=50, null=True)
    added_at = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50)
    owner = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    announcement = models.CharField(max_length=256, null=True)
    avatar = models.CharField(max_length=256, null=True)


class GroupMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    group = models.IntegerField()
    user = models.CharField(max_length=64)
    nickname = models.CharField(max_length=50,null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.IntegerField()


class ContactRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    requester = models.CharField(max_length=64)
    receiver = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )

    def __str__(self):
        return f'Request from {self.requester} to {self.receiver} - Status: {self.status}'

class GptConversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation from {self.user_id}'
    
class Conversation(models.Model):
    CONVERSATION_TYPE_CHOICES = [
        ('P', 'Private'),
        ('G', 'Group'),
    ]
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=1, choices=CONVERSATION_TYPE_CHOICES)
    group = models.IntegerField()
    last_message_at = models.DateTimeField(auto_now_add=True,null=True)

class Participant(models.Model):
    user = models.CharField(max_length=64)
    conversation = models.IntegerField()
    is_hidden=models.BooleanField(default=False)

class GroupJoinRequest(models.Model):
    group = models.IntegerField()
    user = models.CharField(max_length=64)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)