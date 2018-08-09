import json
from datetime import timedelta
from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application
from rest_framework.test import APITestCase


class AuthAPIViewTestCase(APITestCase):
    token_url = '/api/v1/auth/token/'
    revoke_token_url = '/api/v1/auth/revoke-token/'

    def setUp(self):
        self.username = 'john'
        self.email = 'john@snow.com'
        self.password = 'you_know_nothing'
        self.user = User.objects.create_user(username=self.username,
                                             email=self.email,
                                             password=self.password,
                                             is_active=True)
        self.auth_app = Application.objects.create(user=self.user,
                                                   authorization_grant_type='password',
                                                   client_type='public')
        expires_in = timezone.now() + timedelta(minutes=5)
        self.access_token = AccessToken.objects.create(user=self.user,
                                                       token='ZkjjDGPBJ9FtZzWbv6nAw7XiqnGYjH',
                                                       application=self.auth_app,
                                                       expires=str(expires_in))

    def test_get_token_without_password(self):
        response = self.client.post(self.token_url,
                                    urlencode(
                                        {'username': 'snowman@email.local',
                                         'client_id': self.auth_app.client_id,
                                         'client_secret': self.auth_app.client_secret,
                                         'grant_type': 'password'}),
                                    content_type='application/x-www-form-urlencoded')
        self.assertEqual(400, response.status_code)

    def test_get_token_with_wrong_password(self):
        response = self.client.post(self.token_url,
                                    urlencode({'username': self.username,
                                               'password': 'I_know',
                                               'client_id': self.auth_app.client_id,
                                               'client_secret': self.auth_app.client_secret,
                                               'grant_type': 'password'}),
                                    content_type='application/x-www-form-urlencoded')
        self.assertEqual(401, response.status_code)

    def test_get_token_with_valid_data(self):
        response = self.client.post(self.token_url,
                                    urlencode({'username': self.username,
                                               'password': self.password,
                                               'client_id': self.auth_app.client_id,
                                               'client_secret': self.auth_app.client_secret,
                                               'grant_type': 'password'}),
                                    content_type='application/x-www-form-urlencoded')
        self.assertEqual(200, response.status_code)
        self.assertTrue('access_token' in json.loads(response.content))

    def test_revoke_token_with_valid_data(self):
        self.client.credentials(
            Authorization='Bearer {}'.format(self.access_token.token))
        response = self.client.post(self.revoke_token_url,
                                    urlencode(
                                        {'client_id': self.auth_app.client_id,
                                         'client_secret': self.auth_app.client_secret,
                                         'token': self.access_token.token}),
                                    content_type='application/x-www-form-urlencoded')
        self.assertEqual(200, response.status_code)
