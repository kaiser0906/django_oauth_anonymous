'''
This code snippet would not work properly. You may need to change the code below based on your django project structure.
'''

from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from rest_framework import exceptions
from core.tests.base import AuthBaseTestCase
from core.authentications import CustomHeaderAnonymousAuthentication


class CustomHeaderAnonymousAuthenticationTestCase(AuthBaseTestCase):
    '''
    Test custom header for checking client_id as an extra security.
    Also, test with oauth2 authentication and returns AnonymousUser if token is
    invalid rather than returning 401 Unauthorized error.
    '''

    def setUp(self):
        super().setUp()
        self.auth = CustomHeaderAnonymousAuthentication()
        self.factory = RequestFactory()

    def test_authenticate(self):
        request = self.factory.get('/', HTTP_AUTHORIZATION=self.access_token)
#         request.user = self.user
        result = self.auth.authenticate(request)
        self.assertFalse(isinstance(result[0], AnonymousUser))

    def test_authenticate_invalid_token(self):
        request = self.factory.get('/', HTTP_AUTHORIZATION='Bearer foo',
                                   HTTP_X_CLIENT_ID=self.app.client_id)
        result = self.auth.authenticate(request)
        self.assertTrue(isinstance(result[0], AnonymousUser))

    def test_authenticate_invalid_token_no_client_id(self):
        request = self.factory.get('/')
        with self.assertRaises(exceptions.AuthenticationFailed):
            self.auth.authenticate(request)

    def test_authenticate_invalid_token_invalid_client_id(self):
        request = self.factory.get('/', HTTP_X_CLIENT_ID='foo')
        with self.assertRaises(exceptions.AuthenticationFailed):
            self.auth.authenticate(request)
