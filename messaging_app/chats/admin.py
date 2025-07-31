from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "first_name",
        "last_name",
        "email"
    )


class MessageAdmin(admin.ModelAdmin):
    list_display = [
            "message_id",
            "message_body",
            "sent_at",
            "is_read",
            "sender",
            "conversation",
        ]


class ConversationAdmin(admin.ModelAdmin):
    list_display = ["conversation_id", "created_at"]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Conversation, ConversationAdmin)
