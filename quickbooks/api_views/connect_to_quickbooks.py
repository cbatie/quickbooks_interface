import urllib
from django.conf import settings
from django.http.response import JsonResponse
from mesika_utils.RandomTransactionIds import generate_sso_token


def connect_to_quick_books(request):

    response = {}

    try:
        url = settings.CONNECT_QUICKBOOKS
        # random_string = 'cn9zdee5que20qi7idp99x91p2wzt19bee3iy4vr'
        random_string = generate_sso_token()
        params = {'scope': settings.ACCOUNTING_SCOPE, 'redirect_uri': settings.REDIRECT_URI,
                  'response_type': 'code', 'state': random_string, 'client_id': settings.CLIENT_ID}
        url += '?' + urllib.parse.urlencode(params)
        print(url)
        response['status'] = 200
        response['message'] = 'Successful'
        response['access_url'] = url

    except Exception as e:
        response['status'] = 404
        response['Error'] = f'{e.args}'

    return JsonResponse(response)


