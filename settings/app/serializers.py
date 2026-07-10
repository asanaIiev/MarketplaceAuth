from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(user=instance)
        return {
            'detail': 'Successfully logged in',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }