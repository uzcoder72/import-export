from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

import csv
import json
from openpyxl import Workbook

from customer.forms import CustomerModelForm
from customer.models import Customer


class CustomerListView(ListView):
    model = Customer
    template_name = 'customer/customer-list.html'
    context_object_name = 'customer_list'

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        if search_query:
            return Customer.objects.filter(
                Q(full_name__icontains=search_query) | Q(address__icontains=search_query)
            )
        return Customer.objects.all()


class AddCustomerView(CreateView):
    model = Customer
    form_class = CustomerModelForm
    template_name = 'customer/add-customer.html'
    success_url = reverse_lazy('customers')


class EditCustomerView(UpdateView):
    model = Customer
    form_class = CustomerModelForm
    template_name = 'customer/update-customer.html'
    success_url = reverse_lazy('customers')


class DeleteCustomerView(DeleteView):
    model = Customer
    template_name = 'customer/customer-list.html'
    success_url = reverse_lazy('customers')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Customer successfully deleted')
        return super().delete(request, *args, **kwargs)


class ExportDataView(View):
    def get(self, request, *args, **kwargs):
        format = request.GET.get('format', 'csv')
        if format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=customers.csv'
            writer = csv.writer(response)
            writer.writerow(['Id', 'Full Name', 'Email', 'Phone Number', 'Address'])
            for customer in Customer.objects.all():
                writer.writerow([customer.id, customer.full_name, customer.email, customer.phone_number, customer.address])

        elif format == 'json':
            response = HttpResponse(content_type='application/json')
            data = list(Customer.objects.all().values('full_name', 'email', 'phone_number', 'address'))
            response.write(json.dumps(data, indent=4))
            response['Content-Disposition'] = 'attachment; filename=customers.json'

        elif format == 'xlsx':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=customers.xlsx'

            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = 'Customers'

            # Define headers
            headers = ['Id', 'Full Name', 'Email', 'Phone Number', 'Address']
            worksheet.append(headers)

            # Add data rows
            customers = Customer.objects.all().values_list('id', 'full_name', 'email', 'phone_number', 'address')
            for customer in customers:
                worksheet.append(customer)

            # Save workbook to response
            workbook.save(response)

        else:
            response = HttpResponse(status=404)
            response.content = 'Bad request'

        return response
