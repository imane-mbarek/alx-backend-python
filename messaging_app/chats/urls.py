from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from .views import MessageList

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
    path('conversations/<int:conversation_id>/messages/', MessageList.as_view(), name='message-list'),
]
