from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth.mixins import PermissionRequiredMixin

from customer.forms import LoginForm, RegisterModelForm


class LoginPageView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        return self.form_invalid(form)


class LogoutPageView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('customers')


class RegisterPageView(PermissionRequiredMixin, FormView):
    template_name = 'auth/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('customers')
    permission_required = 'customer.add_customer'
    raise_exception = True

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        login(self.request, user)
        return super().form_valid(form)
