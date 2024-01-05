'''Serializers for the User API View'''

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """A Serializer to handle the creation
      and updating of user profiles"""

    class Meta:
        model = get_user_model()  # Use Django's default User model
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Handles creating auth tokens"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        '''Validate and authenticate the user'''
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user or not user.is_active:
            raise serializers.ValidationError(
                _("Invalid credentials"),
                code='authorization'
            )
        attrs['user'] = user
        return attrs
