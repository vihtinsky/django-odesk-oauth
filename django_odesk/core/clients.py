import logging

from odesk import Client
from django.core.exceptions import ImproperlyConfigured
from django_odesk.conf import settings


class DefaultClient(Client):

    def __init__(self, api_token=None):
        public_key = settings.ODESK_PUBLIC_KEY
        secret_key = settings.ODESK_PRIVATE_KEY

        if api_token:
            access_token, access_token_secret = api_token
        else:
            access_token=None
            access_token_secret=None

        if not (public_key and secret_key):
            raise ImproperlyConfigured(
                "The django_odesk.core.clients.DefaultClient requires "+\
                "both ODESK_PUBLIC_KEY and ODESK_PRIVATE_KEY "+\
                "settings to be specified.")

        super(DefaultClient, self).__init__(
            public_key, secret_key, oauth_access_token=access_token,
            oauth_access_token_secret=access_token_secret, auth="oauth")

    def get_user(self):
        return self.hr.get_user('me')

