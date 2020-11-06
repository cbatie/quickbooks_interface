import urllib
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
import json
from django.http.response import JsonResponse

from quickbooks.middleware import (
    get_bearer_token
)


def auth_code_handler(request):
    response = {}
    try:
        request_params = json.loads(request.body)

        web_url = request_params['web_url']
        client_uuid = request_params['client_id']

        auth_res_url = web_url
        start_code = auth_res_url.find('code=') + len('code=')
        end_code = auth_res_url.find('&state')

        start_realm_id = auth_res_url.find('&realmId=') + len('&realmId=')

        auth_code = auth_res_url[start_code:end_code]
        realm_id = auth_res_url[start_realm_id:]

        response = get_bearer_token(auth_code, client_uuid, realm_id)

    except Exception as e:
        response['status'] = 404
        response['Error'] = f'{e.args}'

    return JsonResponse(response)
