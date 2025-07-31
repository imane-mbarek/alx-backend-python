from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings
import uuid
from typing import Union


class UserManager(auth_models.UserManager):

    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: Union[str, None] = None,
        is_staff: bool = False,
        is_superuser=False,
    ) -> "User":

        if not email:
            raise ValueError("User must have an email")

        if not first_name:
            raise ValueError("User must have an first name")

        if not last_name:
            raise ValueError("User must have an last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save()

        return user

    def create_superuser(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
    ) -> "User":

        if not password:
            raise ValueError("Superuser must have a password")

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )

        return user


class User(auth_models.AbstractUser):

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    email = models.EmailField(verbose_name="Email", unique=True, max_length=255)
    phone_number = models.CharField(
        verbose_name="Phone Number", max_length=30, blank=True, null=True
    )
    bio = models.TextField(verbose_name="Bio", blank=True, null=True, max_length=255)
    address = models.CharField(
        verbose_name="Address", max_length=255, blank=True, null=True
    )
    is_admin = models.BooleanField(default=False)  # type: ignore
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"  # set for authentication purpose
    REQUIRED_FIELDS = ["first_name", "last_name"]  # for field when creating superuser

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="conversations"
    )


class Message(models.Model):

    message_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # type: ignore

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="message_sent"
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
