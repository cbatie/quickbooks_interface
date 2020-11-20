import json
from django.http.response import JsonResponse
from ..api_views.customer_request import get_customer_details
from ..models import QuickBooksToken, CorporateInformation
from ..api_views.refresh_token import refresh_token


def customer_details(request):
    response = {}
    try:

        request_params = json.loads(request.body)
        client_account_uuid = request_params['client_uuid']
        customer_account_id = request_params['customer_acct_id']

        corporate_obj = CorporateInformation.objects.get(corporate=client_account_uuid)

        corporate_information = QuickBooksToken.objects.get(corporate=corporate_obj)

        access_token = corporate_information.access_token
        realm_id = corporate_information.realm_id
        refresh_token_old = corporate_information.refresh_token

        quick_books_response = get_customer_details(access_token, realm_id, customer_account_id)

        print(9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
        data_returned = json.loads(quick_books_response.text)
        print(data_returned)
        print(99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)

        if 'warnings' in data_returned or 'fault' in data_returned:
            print('BBBBBBBBBBBBBBBB')
            refresh_old_token = refresh_token(refresh_token_old, client_account_uuid, realm_id)
            print(999999999999999)
            response__ = get_customer_details(refresh_old_token, realm_id, realm_id)
            new_request_response = json.loads(response__.text)
            print(8888888888888888)

        else:
            print(5555555555555555555)
            new_request_response = data_returned

            print(new_request_response['Customer']['DisplayName'])

            customer_data = []

            if new_request_response and new_request_response['Customer']:

                name = new_request_response['Customer']['DisplayName']
                account_number = name.split(' ', 1)[0]
                customer_name = ' '.join(name.split()[1:])

                try:
                    company_name = new_request_response['Customer']['CompanyName']
                except:
                    company_name = 'No Company Name'
                   
                try:
                    customer_email = new_request_response['Customer']['PrimaryEmailAddr']['Address']
                except:
                    customer_email = 'No Email'

                data = {
                         'company_name': company_name,
                         'name': customer_name,
                         'email': customer_email,
                         'account_number': account_number,
                         'phone_number': new_request_response['Customer']['PrimaryPhone']['FreeFormNumber']

                       }

                # customer_data.append(data)
                response['status'] = 200
                response = data

            else:
                data = {
                    'company_name': 'N/A',
                    'name': 'N/A',
                    'email': 'N/A',
                    'account_number': 'N/A',
                    'phone_number': 'N/A',

                }

                # customer_data.append(data)

                response['status'] = 200
                response = data


    except Exception as e:
            response['status'] = 501
            response['message'] = f'{e.args}'

    return JsonResponse(response)
