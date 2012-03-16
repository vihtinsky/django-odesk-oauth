import logging
import datetime

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django_odesk.core.clients import DefaultClient
from django_odesk.auth import (
    ODESK_REDIRECT_SESSION_KEY, ODESK_REQUEST_TOKEN, ODESK_ACCESS_TOKEN
)



def authenticate(request):
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    request.session[ODESK_REDIRECT_SESSION_KEY] = redirect_to
    odesk_client = DefaultClient()
    request.session[ODESK_REQUEST_TOKEN] = odesk_client.auth.get_request_token()
    return HttpResponseRedirect(odesk_client.auth.get_authorize_url())


def callback(request, redirect_url=None):
    odesk_client = DefaultClient()
    if request.session.get(ODESK_REQUEST_TOKEN):
        t, s = request.session.get(ODESK_REQUEST_TOKEN)
        odesk_client.auth.request_token = t
        odesk_client.auth.request_token_secret = s
        del request.session[ODESK_REQUEST_TOKEN]
    else:
        return HttpResponseRedirect(odesk_client.auth.get_authorize_url())

    verifer = request.GET.get('oauth_verifier', None)
    access_token = odesk_client.auth.get_access_token(verifer)

    if access_token:
        request.session[ODESK_ACCESS_TOKEN] = access_token
        #TODO: Get rid of (conceptually correct) additional request to odesk.com
        user = django_authenticate(token = access_token)
        if user:
            login(request, user)
        else:
            pass
            #Probably the odesk auth backend is missing. Should we raise an error?
        redirect_url = request.session.pop(ODESK_REDIRECT_SESSION_KEY,
                                           redirect_url)
        response = HttpResponseRedirect(redirect_url or '/')
        return response
    else:
        return HttpResponseRedirect(odesk_client.auth.get_authorize_url())

