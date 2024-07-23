# customer/signals.py

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import json
from customer.models import Customer

@receiver(post_save, sender=Customer)
def send_email_on_customer_creation(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our Service'
        message = f'Hi {instance.full_name},\n\nThank you for registering with us. We are glad to have you on board.'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])

@receiver(pre_delete, sender=Customer)
def save_customer_details_before_deletion(sender, instance, **kwargs):
    customer_data = {
        'full_name': instance.full_name,
        'email': instance.email,
        'phone_number': instance.phone_number,
        'address': instance.address,
        'joined': instance.joined.strftime('%Y-%m-%d %H:%M:%S'),
    }
    with open('deleted_customers.json', 'a') as f:
        json.dump(customer_data, f)
        f.write('\n')
