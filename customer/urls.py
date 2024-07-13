from django.urls import path

from customer.views.auth import LoginPageView, LogoutPageView, RegisterPageView
from customer.views.customers import CustomerListView, AddCustomerView, EditCustomerView, DeleteCustomerView, ExportDataView

urlpatterns = [
    path('customer-list/', CustomerListView.as_view(), name='customers'),
    path('add-customer/', AddCustomerView.as_view(), name='add_customer'),
    path('customer/<int:pk>/delete', DeleteCustomerView.as_view(), name='delete'),
    path('customer/<int:pk>/update', EditCustomerView.as_view(), name='edit'),
    # Authentication path
    path('login-page/', LoginPageView.as_view(), name='login'),
    path('logout-page/', LogoutPageView.as_view(), name='logout'),
    path('register-page/', RegisterPageView.as_view(), name='register'),
    path('export-data/', ExportDataView.as_view(), name='export_data')
]
