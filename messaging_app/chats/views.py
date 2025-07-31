from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from .permissions import IsParticipantOfConversation, IsParticipant
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    UserSerializer
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .filters import MessageFilter
from .pagination import MessagePagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation, IsParticipant]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)    

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation, IsParticipant]
    pagination_class = MessagePagination  # Add this
    filter_backends = [DjangoFilterBackend]  # Add this
    filterset_class = MessageFilter  # Add this

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=self.request.user
        )
        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=self.request.user
        )
        serializer.save(
            conversation=conversation,
            sender=self.request.user
        )
        
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)