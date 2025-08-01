import django_filters
from django.db import models
from .models import Message


class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.NumberFilter(field_name='conversation__id')
    sender = django_filters.NumberFilter(field_name='sender__id')
    receiver = django_filters.NumberFilter(field_name='receiver__id')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = {
            'content': ['icontains'],
        }

    @property
    def qs(self):
        parent = super().qs
        # Add any additional filtering logic here if needed
        return parent