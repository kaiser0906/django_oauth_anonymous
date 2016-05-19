from django.contrib.auth.models import AnonymousUser
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.models import Application
from rest_framework import exceptions


class CustomHeaderAnonymousAuthentication(OAuth2Authentication):
    '''
    Checks valid token and authenticate user first. If token is invalid,
    returns user as AnonymousUser.
    This class helps visibility of public and private shared assets based on
    the status of authentication.
    '''
    def authenticate(self, request):
        '''
        X-CLIENT-ID header is required and corresponding `Application` must
        exist in the system. returns 401 otherwise.
        '''
        auth = super().authenticate(request)
        if auth:
            return auth
        else:
            client_id = request.META.get('HTTP_X_CLIENT_ID')
            if not client_id:
                raise exceptions.AuthenticationFailed()
            try:
                application = Application.objects.get(client_id=client_id)
            except Application.DoesNotExist:
                raise exceptions.AuthenticationFailed()
            else:
                request.application = application
            return AnonymousUser(), None

    def authenticate_header(self, request):
        '''
        forces 401 instead of 403 by not returning None
        '''
        return 'Custom Header'
