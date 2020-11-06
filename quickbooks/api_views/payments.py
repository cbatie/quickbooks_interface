import json
from django.http.response import JsonResponse
from ..models import QuickBooksToken, CorporateInformation
from ..api_views.payment_request import connect_to_quick_books
from ..api_views.refresh_token import refresh_token


def invoice_payment(request):
    response = {}
    try:

        request_params = json.loads(request.body)
        client_account_uuid = request_params['client_uuid']
        print(client_account_uuid)

        corporate_obj = CorporateInformation.objects.get(corporate=client_account_uuid)

        if corporate_obj:
            corporate_information = QuickBooksToken.objects.get(corporate=corporate_obj)

            access_token = corporate_information.access_token
            realm_id = corporate_information.realm_id
            refresh_token_old = corporate_information.refresh_token

            print('222222222222222222222222222222222222222222222222222')
            print(realm_id)
            print(access_token)
            data_from_quick_books = connect_to_quick_books(access_token, realm_id)
            data_returned = json.loads(data_from_quick_books.text)

            print(data_from_quick_books)
            print(refresh_token_old)

            if 'warnings' in data_returned or 'fault' in data_returned:
                print('BBBBBBBBBBBBBBBB')
                refresh_old_token = refresh_token(refresh_token_old, client_account_uuid, realm_id)
                print(999999999999999)
                new_request_response = connect_to_quick_books(refresh_old_token, realm_id)
                print(8888888888888888)

            else:
                print(5555555555555555555)
                new_request_response = data_from_quick_books

            print(4444444444444444444444)
            data_returned = json.loads(new_request_response.text)


            loop_data = data_returned['QueryResponse']['Payment']
            print(loop_data)
            print(loop_data[0])

            # Sandbox = settings.CUSTOMER_ENDPOINT + realm_id + "/customer/{0}?minorversion=54".format(customer_id)
            # quick_books_response = get_customer_details(access_token, realm_id, customer_id=58)
            # print(9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
            # print(json.loads(quick_books_response.text))
            # print(99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)

            quick_books_customer_data = []

            for data in loop_data:
                try:
                    pay_ref = data['PaymentRefNum']
                except:
                    pay_ref ='no payment ref'

                try:
                    pay_type = data['LinkedTxn'][0]['TxnType']
                except:
                    pay_type = 'no payment type'

                quick_books_data = {

                    'date': data['TxnDate'],
                    'provider_name': 'N/A',
                    'payment_id': data['Id'],
                    'bank_amount': data['TotalAmt'],
                    'amount': data['TotalAmt'],
                    'reference': pay_ref,
                    'currency_rate': data['CurrencyRef']['value'],
                    'payment_type': pay_type,
                    'status_xero': 'N/A',
                    'account_id': data['CustomerRef']['value'],
                    'customer_contact_id': data['CustomerRef']['value'],
                    'invoice_type': pay_type,
                    'invoice_id': data['Id'],
                    'invoice_number': pay_ref,

                }

                quick_books_customer_data.append(quick_books_data)

            response['status'] = 200
            response['erp_payment_data'] = quick_books_customer_data
        else:
            pass
    except Exception as e:
        response['status'] = 200
        response['message'] = e.args

    return JsonResponse(response)

