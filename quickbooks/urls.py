from django.urls import path

from .api_views.connect_to_quickbooks import connect_to_quick_books
from .api_views.auth_handler import auth_code_handler
from .api_views.payments import invoice_payment
from .api_views.customer import customer_details

urlpatterns = [
    path('connect_to_quick_books/', connect_to_quick_books, name="connect_to_quick_books"),
    path('complete_connection/', auth_code_handler, name='complete_connection'),
    path('all_payments/', invoice_payment, name='payments'),

    path('get_customer/', customer_details)
]
