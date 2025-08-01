from rest_framework import viewsets, status, filters, generics, permissions
from django_filters import rest_framework as django_filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    UserSerializer
)
from .permissions import (
    IsConversationParticipant,
    IsMessageOwner,
    IsParticipantOrAdmin,
    IsParticipant
)
from .filters import MessageFilter
from .pagination import MessagePagination
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversation model with custom permissions and filtering.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    ordering_fields = ['created_at', 'updated_at']
    search_fields = ['participants__username']
    permission_classes = [permissions.IsAuthenticated, IsParticipantOrAdmin]

    def get_queryset(self):
        """
        Return conversations where current user is a participant,
        ordered by most recent activity.
        """
        user = self.request.user
        return Conversation.objects.filter(
            participants=user
        ).order_by('-updated_at')

    def perform_create(self, serializer):
        """
        Automatically add the current user as a participant
        when creating a conversation.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """
        Custom action to add participants to an existing conversation.
        """
        conversation = self.get_object()
        participant_id = request.data.get('user_id')

        if not participant_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(pk=participant_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if conversation.participants.filter(pk=user.pk).exists():
            return Response(
                {"error": "User is already a participant"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation.participants.add(user)
        return Response(
            {"status": "participant added"},
            status=status.HTTP_200_OK
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message model with pagination, filtering, and custom permissions.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_class = MessageFilter
    ordering_fields = ['timestamp', 'created_at']
    search_fields = ['content']
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        Return messages in conversations where current user is a participant,
        with optional filtering by conversation ID.
        """
        user = self.request.user
        conversation_id = self.request.query_params.get('conversation_id')

        queryset = Message.objects.filter(
            Q(conversation__participants=user) |
            Q(sender=user)
        ).distinct().order_by('-timestamp')

        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)

        return queryset

    def perform_create(self, serializer):
        """
        Automatically set the sender to the current user
        and mark as unread for other participants.
        """
        conversation_id = self.request.data.get('conversation_id')
        conversation = Conversation.objects.get(id=conversation_id)
        message = serializer.save(sender=self.request.user, conversation=conversation)

        # Mark as unread for all participants except sender
        conversation.participants.exclude(
            pk=self.request.user.pk
        ).update(unread_messages=True)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Custom action to mark a message as read.
        """
        message = self.get_object()
        if request.user in message.conversation.participants.all():
            message.is_read = True
            message.save()
            return Response(
                {"status": "message marked as read"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Not a participant in this conversation"},
            status=status.HTTP_403_FORBIDDEN
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User model (read-only).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']