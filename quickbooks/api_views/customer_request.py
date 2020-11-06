import requests
from django.conf import settings


def get_customer_details(access_token, realm_id, customer_id):

    auth_header = 'Bearer ' + access_token

    headers = {'Accept': 'application/json', 'Authorization': auth_header, 'Content-Type': 'application/json'}

    url = settings.CUSTOMER_ENDPOINT + realm_id + "/customer/{0}?minorversion=54".format(customer_id)

    quick_books_response = requests.get(url, headers=headers)

    return quick_books_response

