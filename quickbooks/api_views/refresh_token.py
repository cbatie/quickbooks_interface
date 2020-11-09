import requests
import base64
import json
import random
from datetime import datetime
from django.conf import settings
from ..models import QuickBooksToken, CorporateInformation


def string_to_Base64(s):
    return base64.b64encode(bytes(s, 'utf-8')).decode()


def refresh_token(refresh_client_token, corporate, realm_id):
    # token_endpoint = getDiscoveryDocument.token_endpoint
    token_endpoint = settings.REFRESH_TOKEN
    print('in revoke token')
    print(token_endpoint)
    auth_header = 'Basic ' + string_to_Base64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded',
               'Authorization': auth_header}
    payload = {
        'refresh_token': refresh_client_token,
        'grant_type': 'refresh_token'
    }
    r = requests.post(token_endpoint, data=payload, headers=headers)
    bearer_raw = json.loads(r.text)

    if 'id_token' in bearer_raw:
        idToken = bearer_raw['id_token']
    else:
        idToken = None

    x_refresh_token_expires_in = bearer_raw['x_refresh_token_expires_in']
    access_token = bearer_raw['access_token']
    token_type = bearer_raw['token_type']
    refresh_token_ = bearer_raw['refresh_token']
    expires_in = bearer_raw['expires_in']

    corporate_profile = CorporateInformation.objects.filter(corporate=corporate).first()

    access_information = QuickBooksToken.objects.filter(corporate=corporate_profile.corporate_uuid).update(
        refresh_token=refresh_token_, access_token=access_token, access_token_expire=expires_in,
        refresh_token_expire=x_refresh_token_expires_in, token_type=token_type)
    print(access_information)

    return access_token
