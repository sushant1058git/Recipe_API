"""
Test for the user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create') #app:endpoint
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    """Create and return new User."""

    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API (features which does not requires authentication)"""

    def setUp(self):
        self.client=APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""

        payload={
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test Name'
        }
        res=self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user=get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)


    def test_user_email_exists(self):
        """Test error returned if user email already exists"""

        payload={
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test Name'
        }
        create_user(**payload)
        res=self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""
        user_details = {
            'name':'testname',
            'email':'test@example.com',
            'password':'password'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password':user_details['password'],

        }

        res=self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_bad_credentials(self):
        """Test return error if credentials are invalid"""

        create_user(email='test@test.com', password='pass1234')

        payload = {
            'email':'test@test.com',
            'password':'pass2345'
        }
        res= self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUsersAPITests(TestCase):
    """Test API requests that require authetication"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password = 'testpass123',
            name = 'Test Name'
        )

        self.client  = APIClient()
        self.client.force_authenticate(user= self.user)


    def test_retrieve_profile_succes(self):
        """Test retrieving profile Scuss"""

        res=self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name':self.user.name,
            'email':self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed on ME_URL"""
        res=self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test Updating the user profile for the autheticated user"""
        payload = {'name':'Updated name', 'password' : 'newpass123'}

        res=self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)