import django_filters
from .models import Message
from django.utils import timezone


class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__user_id')
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']
