# messaging_app/chats/permissions.py
from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsAuthenticated(permissions.IsAuthenticated):
    """
    Ensures only authenticated users can access the API.
    This overrides DRF's default to provide clearer messaging.
    """
    message = 'Only authenticated users can access this resource.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsParticipant(BasePermission):
    """
    Checks if user is a participant in the conversation.
    Applies to all message operations (send, view, update, delete).
    """
    message = 'You must be a participant of this conversation.'

    def has_object_permission(self, request, view, obj):
        # For Message objects
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        # For Conversation objects
        elif hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False


class IsMessageOwner(BasePermission):
    """
    Checks if the user is the owner of the message.
    """
    message = 'You must be the message owner to perform this action.'

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsParticipantOrAdmin(BasePermission):
    """
    Allows access to participants or admin users.
    """
    message = 'You must be a participant or admin to access this resource.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # For Message objects
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        # For Conversation objects
        elif hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False


class IsConversationParticipant(BasePermission):
    """
    Specifically checks if user is a participant of the conversation.
    """
    message = 'You must be a participant of this conversation.'

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsMessageOwnerOrParticipant(BasePermission):
    """
    Combines ownership and participation checks for messages.
    - Allows participants to view messages
    - Only allows message owner to modify/delete
    """
    message = 'You must be the message owner to perform this action.'

    def has_object_permission(self, request, view, obj):
        # Always allow safe methods (GET, HEAD, OPTIONS) for participants
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.conversation.participants.all()

        # Only allow modification by the sender
        return obj.sender == request.user


class ReadOnlyOrIsParticipant(BasePermission):
    """
    Allows read-only access to all participants,
    but restricts write operations to specific conditions.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS for all participants
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.conversation.participants.all()

        # Only allow PUT, PATCH, DELETE for message owner
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.sender == request.user

        return False


class ConversationPermissions(BasePermission):
    """
    Special permissions for conversation operations:
    - Anyone can create conversations
    - Only participants can view
    - Only participants can add other participants
    - No one can delete conversations (or implement your business logic)
    """
    def has_permission(self, request, view):
        # Allow conversation creation
        if request.method == 'POST':
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        # Allow all participants to view
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.participants.all()

        # Special handling for participant addition
        if request.method in ['PUT', 'PATCH']:
            return request.user in obj.participants.all()

        # By default, no deletion allowed
        if request.method == 'DELETE':
            return False

        return False