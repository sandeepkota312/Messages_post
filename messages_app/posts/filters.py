from .models import Messages
import django_filters

class MessageFilter(django_filters.FilterSet):
    class Meta:
        model=Messages
        fields=['user','title',]