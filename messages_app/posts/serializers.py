from rest_framework import serializers
from .models import Messages
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Messages
        fields=['user','id','title','message','likes','count']



