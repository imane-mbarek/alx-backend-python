from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Conversation, Message
from django.utils.translation import gettext_lazy as _


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)  # Safely remove username field

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                _('Both email and password are required'),
                code='authorization'
            )

        # Map email to username for parent class validation
        attrs['username'] = email

        try:
            data = super().validate(attrs)
        except Exception as e:
            raise serializers.ValidationError(
                _('Invalid email or password'),
                code='authorization'
            )

        # Add custom claims
        data.update({
            'user_id': str(self.user.id),
            'email': self.user.email
        })
        return data

class UserSerializer(serializers.ModelSerializer):
    extra_note = serializers.CharField(required=False, default="")

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number']  # Removed username/first_name/last_name as your model doesn't have them
        extra_kwargs = {
            'id': {'read_only': True}
        }


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    formatted_sent_at = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation', 'content', 'timestamp', 'formatted_sent_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'timestamp': {'read_only': True}
        }

    def get_formatted_sent_at(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages.all')

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at', 'messages', 'is_group', 'name']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def validate(self, data):
        if 'participants' in data and len(data['participants']) < 2:
            raise serializers.ValidationError(
                "A conversation must include at least two participants."
            )
        return data