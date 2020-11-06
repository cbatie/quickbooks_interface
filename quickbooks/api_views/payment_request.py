import requests
from django.conf import settings


def connect_to_quick_books(access_token, realm_id):

    auth_header = 'Bearer ' + access_token

    headers = {'Accept': 'application/json', 'Authorization': auth_header, 'Content-Type': 'application/json'}

    url = settings.INVOICE_PAYMENT_START + realm_id + settings.INVOICE_PAYMENT_END

    quick_books_response = requests.get(url, headers=headers)

    return quick_books_response

