"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        inputs = {
        'email': 'test@example.com',
        'password': 'testpass123'}
        user = get_user_model().objects.create_user(
            email=inputs['email'],
            password=inputs['password']
        )

        self.assertEqual(user.email, inputs['email'])
        self.assertTrue(user.check_password(inputs['password']))
