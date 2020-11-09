import requests
import base64
import json
import random

# from jose import jwk
from datetime import datetime

from django.conf import settings

# from sampleAppOAuth2 import getDiscoveryDocument
from quickbooks.models import CorporateInformation, QuickBooksToken
# from quickbooks import QuickBooks
# from intuitlib.client import AuthClient


# token can either be an accessToken or a refreshToken
def revoke_token(token):
    revoke_endpoint = settings.REVOKE_TOKEN
    auth_header = 'Basic ' + stringToBase64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'content-type': 'application/json', 'Authorization': auth_header}
    payload = {'token': token}
    r = requests.post(revoke_endpoint, json=payload, headers=headers)

    if r.status_code >= 500:
        return 'internal_server_error'
    elif r.status_code >= 400:
        return 'Token is incorrect.'
    else:
        return 'Revoke successful'


def get_bearer_token(auth_code, corporate_uuid, realm_id):
    token_endpoint = settings.BEARER_TOKEN
    auth_header = 'Basic ' + stringToBase64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded',
               'Authorization': auth_header}

    response = {}

    print(auth_code)
    print(realm_id)
    payload = {
        'code': auth_code,
        'redirect_uri': settings.REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    r = requests.post(token_endpoint, data=payload, headers=headers)

    bearer_raw = json.loads(r.text)
    print(r.status_code)
    if r.status_code != 200 or 'access_token' not in bearer_raw:
        print(bearer_raw)
        response['status'] = 404
        response['message'] = 'Invalid Token'
        response['error'] = bearer_raw['error_description']
    elif r.status_code == 200:

        # print(bearer_raw)
        #
        # if 'id_token' in bearer_raw:
        #     response = bearer_raw['id_token']
        # else:
        #     response = None

        refresh_token = bearer_raw['refresh_token']
        access_token = bearer_raw['access_token']
        x_refresh_token_expires_in = bearer_raw['x_refresh_token_expires_in']
        token_type = bearer_raw['token_type']
        expires_in = bearer_raw['expires_in']
        # id_token = bearer_raw['idToken']

        corporate_profile = CorporateInformation(corporate=corporate_uuid)
        corporate_profile.save()

        access_information = QuickBooksToken(corporate=corporate_profile, refresh_token=refresh_token,
                                             access_token=access_token, access_token_expire=expires_in,
                                             refresh_token_expire=x_refresh_token_expires_in, token_type=token_type,
                                             realm_id=realm_id)
        access_information.save()

        # print(pp)
        # print(kk)
        response['status'] = 200
        response['message'] = 'Corporate Connected To QuickBooks Successfully'
        response['tenant_id'] = realm_id
    else:
        response['status'] = 404
        response['message'] = bearer_raw

    return response


def get_bearer_token_from_refresh_token(refresh_token):

    token_endpoint = settings.BEARER_TOKEN

    auth_header = 'Basic ' + stringToBase64(settings.CLIENT_ID + ':' + settings.CLIENT_SECRET)
    headers = {'Accept': 'application/json', 'content-type': 'application/x-www-form-urlencoded',
               'Authorization': auth_header}
    payload = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    r = requests.post(token_endpoint, data=payload, headers=headers)
    bearer_raw = json.loads(r.text)

    if 'id_token' in bearer_raw:
        idToken = bearer_raw['id_token']
    else:
        idToken = None

    return Bearer(bearer_raw['x_refresh_token_expires_in'], bearer_raw['access_token'], bearer_raw['token_type'],
                  bearer_raw['refresh_token'], bearer_raw['expires_in'], idToken=idToken)


def getUserProfile(access_token, realmId, refresh_token):
    auth_header = 'Bearer ' + access_token
    headers = {'Accept': 'application/json', 'Authorization': auth_header, 'Content-Type': 'application/json'}
    r = requests.get(settings.SANDBOX_PROFILE_URL, headers=headers)
    status_code = r.status_code
    response = json.loads(r.text)

    data = {
        "TotalAmt": 28.0,
        "CustomerRef": {
        "value": "20"
        }
    }

    INVOICE = 'https://sandbox-quickbooks.api.intuit.com/v3/company/{0}/payment'.format(realmId)
    rrr = "https://sandbox-quickbooks.api.intuit.com/v3/company/{0}/invoice".format(realmId)
    rr = requests.get(INVOICE, data=json.dumps(data), headers=headers)
    print('111111111111')
    print(rr.json())
    print(realmId)
    print('2222222222222222')

    # qbObject = QuickBooks(
    #     consumer_key=settings.CLIENT_ID,
    #     consumer_secret=settings.CLIENT_SECRET,
    #     callback_url=settings.REDIRECT_URI,
    # )
    # print(json.loads(qbObject))
    # authorize_url = qbObject.get_authorize_url()

    # print(authorize_url)

    # auth_client = AuthClient(
    #     client_id=settings.CLIENT_ID,
    #     client_secret=settings.CLIENT_SECRET,
    #     environment='sandbox',
    #     redirect_uri=settings.REDIRECT_URI,
    # )
    #
    # client = QuickBooks(
    #     auth_client=auth_client,
    #     refresh_token=refresh_token,
    #     company_id=settings.CLIENT_ID,
    #     minorversion=4
    # )
    #
    # from quickbooks.cdc import change_data_capture
    # from quickbooks.objects import Invoice
    #
    # cdc_response = change_data_capture([Invoice], "2017-01-01T00:00:00", qb=client)
    #
    # from quickbooks.objects.customer import Customer
    # customers = Customer.all(qb=client)
    # print(customers)

    opt = "https://sandbox-quickbooks.api.intuit.com/v3/company/4620816365150925190/query?query=select%20*%20from%20Payment%20Where%20Metadata.LastUpdatedTime%3E%272015-01-16%27%20OrderBy%20Metadata.LastUpdatedTime&minorversion=54"
    rrr = requests.get(opt, headers=headers)
    print(rrr.json())
    # "https://sandbox.api.intuit.com"

    rrr4 = "https://sandbox-quickbooks.api.intuit.com/quickbooks/v4/customers/25/bank-accounts"
    print('33333333333333333333333333333333333333333333333333')
    opt2 = requests.get(rrr4, headers=headers)
    print(opt2)
    return response, status_code


def getCompanyInfo(access_token, realmId):
    route = '/v3/company/{0}/companyinfo/{0}'.format(realmId)
    auth_header = 'Bearer ' + access_token
    headers = {'Authorization': auth_header, 'accept': 'application/json'}
    r = requests.get(settings.SANDBOX_QBO_BASEURL + route, headers=headers)
    status_code = r.status_code
    if status_code != 200:
        response = ''
        return response, status_code
    response = json.loads(r.text)
    return response, status_code


# The validation steps can be found at ours docs at developer.intuit.com
# def validateJWTToken(token):
#     current_time = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
#     token_parts = token.split('.')
#     idTokenHeader = json.loads(base64.b64decode(token_parts[0]).decode('ascii'))
#     idTokenPayload = json.loads(base64.b64decode(incorrect_padding(token_parts[1])).decode('ascii'))
#
#     if idTokenPayload['iss'] != settings.ID_TOKEN_ISSUER:
#         return False
#     elif idTokenPayload['aud'][0] != settings.CLIENT_ID:
#         return False
#     elif idTokenPayload['exp'] < current_time:
#         return False
#
#     token = token.encode()
#     token_to_verify = token.decode("ascii").split('.')
#     message = token_to_verify[0] + '.' + token_to_verify[1]
#     idTokenSignature = base64.urlsafe_b64decode(incorrect_padding(token_to_verify[2]))
#
#     keys = getKeyFromJWKUrl(idTokenHeader['kid'])
#
#     publicKey = jwk.construct(keys)
#     return publicKey.verify(message.encode('utf-8'), idTokenSignature)


def getKeyFromJWKUrl(kid):
    # jwk_uri = getDiscoveryDocument.jwks_uri
    jwk_uri = settings.JWT_KEY
    r = requests.get(jwk_uri)
    if r.status_code >= 400:
        return ''
    data = json.loads(r.text)

    key = next(ele for ele in data["keys"] if ele['kid'] == kid)
    return key


# for decoding ID Token
def incorrect_padding(s):
    return s + '=' * (4 - len(s) % 4)


def stringToBase64(s):
    return base64.b64encode(bytes(s, 'utf-8')).decode()


# Returns a securely generated random string. Source from the django.utils.crypto module.
def getRandomString(length, allowed_chars='abcdefghijklmnopqrstuvwxyz' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))


# Create a random secret key. Source from the django.utils.crypto module.
def getSecretKey():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return getRandomString(40, chars)
