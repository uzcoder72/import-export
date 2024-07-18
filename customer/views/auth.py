from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from customer.forms import LoginForm, RegisterModelForm
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from customer.token_generator import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.contrib.auth import login
from django.views import View
from django.shortcuts import render, redirect

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




class RegisterPageView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.is_active = False  # Deactivate account until it is confirmed
        user.save()

        # Send activation email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = self.request.build_absolute_uri(
            reverse('activate', kwargs={'uidb64': uid, 'token': token})
        )

        subject = 'Activate Your Account'
        message = f'Hi {user.username}, please use the link below to activate your account:\n{activation_link}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return super().form_valid(form)


User = get_user_model()

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('customers')
        else:
            return render(request, 'activation_invalid.html')

