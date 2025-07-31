from rest_framework import routers 
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet, UserListCreate, UserDetails #, UserViewSet
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(nested_router.urls)),
    path("users/", UserListCreate.as_view()),
    path("users/<int:pk>/", UserDetails.as_view(), name="user-details")
]
