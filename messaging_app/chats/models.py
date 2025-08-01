import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser with additional fields.
    Uses UUID as primary key for better security and distributed systems compatibility.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A user with that email already exists."
        }
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        validators=[MinLengthValidator(10)]
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
    last_active = models.DateTimeField(
        default=timezone.now
    )
    is_online = models.BooleanField(
        default=False
    )

    # Remove these fields from AbstractUser as we're using email as primary identifier
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
        ]


class Conversation(models.Model):
    """
    Represents a conversation between multiple users.
    Tracks creation, updates, and unread status for participants.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations',
        through='ConversationParticipant'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    is_group = models.BooleanField(
        default=False
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        if self.name:
            return self.name
        participants = self.participants.all()[:3]
        names = [user.email for user in participants]
        if self.participants.count() > 3:
            names.append('...')
        return f"Conversation with {', '.join(names)}"

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['updated_at']),
        ]


class ConversationParticipant(models.Model):
    """
    Through model for Conversation participants with additional metadata.
    Tracks unread messages and notification preferences per participant.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversation_participants'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='conversation_participants'
    )
    joined_at = models.DateTimeField(
        auto_now_add=True
    )
    unread_count = models.PositiveIntegerField(
        default=0
    )
    is_muted = models.BooleanField(
        default=False
    )
    is_admin = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = ('user', 'conversation')
        indexes = [
            models.Index(fields=['user', 'conversation']),
        ]


class Message(models.Model):
    """
    Represents a message in a conversation with various status flags.
    Supports different message types (text, image, etc.) and read receipts.
    """
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    FILE = 'file'
    MESSAGE_TYPES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (FILE, 'File'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_messages'
    )
    content = models.TextField()
    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPES,
        default=TEXT
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    is_read = models.BooleanField(
        default=False
    )
    is_edited = models.BooleanField(
        default=False
    )
    is_deleted = models.BooleanField(
        default=False
    )
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies'
    )
    attachment = models.FileField(
        upload_to='message_attachments/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.sender.email if self.sender else 'Deleted User'}: {self.content[:50]}"

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['conversation', 'timestamp']),
            models.Index(fields=['sender', 'timestamp']),
        ]


class MessageReadReceipt(models.Model):
    """
    Tracks which users have read specific messages for read receipts.
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='read_receipts'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_read_receipts'
    )
    read_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('message', 'user')
        verbose_name = 'Message Read Receipt'
        verbose_name_plural = 'Message Read Receipts'