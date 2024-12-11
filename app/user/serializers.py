"""
Serializers for the user API view.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate
    )
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User objects"""

    # meta class descripts the model
    class Meta:
        model = get_user_model()
        # These fields we want to be available in the serializer.
        # Only allow fields that you want the users to be able to change
        fields = ['email', 'password', 'name']
        # don't allow anyone to read the password,
        # must be more than 5 characters
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password.
        Overrides the default create method so that we can use
        our creat_user method that encrypts the pw"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with the provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
