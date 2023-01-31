from django.shortcuts import get_object_or_404
from rest_framework import serializers
from yamdb.models import User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        required=True, max_length=150, regex=r'^[\w.@+-]+$')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('me - not allowed username')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        required=True, max_length=150, regex=r'^[\w.@+-]+$')
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user:
            if user.confirmation_code == data['confirmation_code']:
                return data
            raise serializers.ValidationError('Wrong Code')
        raise serializers.ValidationError('User not exists')
