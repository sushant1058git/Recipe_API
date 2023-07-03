"""
Test for models """

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""

        email='test@example.com'
        password='pass223'

        user=get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_user_email(self):
        """Test email is normalized for user"""

        sample_emails=[
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com','Test2@example.com'],
            ['TEST3@Example.com','TEST3@example.com']
        ]

        for email, excepted in sample_emails:
            user=get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, excepted)

    def test_new_user_without_an_email(self):
        """Test that creating an user withput an email raise ValueError"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test')


    def test_create_superuser(self):
        """Test creating a superuser"""

        user=get_user_model().objects.create_superuser('test@example.com', 'test123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)