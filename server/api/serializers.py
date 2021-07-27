from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSuggestionSerializer(serializers.ModelSerializer):
    class Meta: 
        model=UserSuggestion
        fields='__all__'