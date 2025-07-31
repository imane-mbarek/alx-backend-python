from rest_framework import permissions
from .models import Conversation
from rest_framework.exceptions import PermissionDenied

class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(user_id=request.user.user_id).exists()


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants of a conversation to access it
    """
    
    def has_permission(self, request, view):
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
            
        # For message creation, check conversation participation
        if view.action == 'create':
            conversation_id = view.kwargs.get('conversation_pk')
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                if request.user not in conversation.participants.all():
                    raise PermissionDenied("You are not a participant of this conversation")
            except Conversation.DoesNotExist:
                raise PermissionDenied("Conversation not found")
        return True

    def has_object_permission(self, request, view, obj):
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
            
        # For PUT, PATCH, DELETE - verify user is participant
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if request.user not in obj.conversation.participants.all():
                raise PermissionDenied("You are not a participant of this conversation")
        return True

# class IsParticipantOfConversation(permissions.BasePermission):
#     """
#     Allow only participants of a conversation to access it
#     """
#     def has_permission(self, request, view):
#         # Ensure user is authenticated
#         if not request.user.is_authenticated:
#             return False
            
#         # For message creation, check conversation participation
#         if view.action == 'create':
#             conversation_id = view.kwargs.get('conversation_pk')
#             try:
#                 conversation = Conversation.objects.get(id=conversation_id)
#                 return request.user in conversation.participants.all()
#             except Conversation.DoesNotExist:
#                 return False
#         return True

#     def has_object_permission(self, request, view, obj):
#         # Ensure user is authenticated
#         if not request.user.is_authenticated:
#             return False
            
#         # For PUT, PATCH, DELETE - verify user is participant
#         if request.method in ['PUT', 'PATCH', 'DELETE']:
#             return request.user in obj.conversation.participants.all()
#         return True