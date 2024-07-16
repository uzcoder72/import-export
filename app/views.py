from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from django.shortcuts import render, redirect
from app.forms import EmailForm, SMSForm, ProductModelForm
from app.models import Product

# Create your views here.


def index(request):
    page = request.GET.get('page', '')
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 2)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj
    }
    return render(request, 'app/index.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    attributes = product.get_attributes()

    context = {
        'product': product,
        'attributes': attributes
    }
    return render(request, 'app/product-detail.html', context)


# def add_product(request):
#     form = ProductForm()
#     # form = None
#     if request.method == 'POST':
#
#         name = request.POST['name']
#         description = request.POST['description']
#         price = request.POST['price']
#         rating = request.POST['rating']
#         discount = request.POST['discount']
#         quantity = request.POST['quantity']
#         form = ProductForm(request.POST)
#         product = Product(name=name, description=description, price=price, discount=discount, quantity=quantity,
#                           rating=rating)
#
#         if form.is_valid():
#             product.save()
#             return redirect('index')
#
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'app/add-product.html', context)


def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form': form,
    }
    return render(request, 'app/add-product.html', context)




def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient = form.cleaned_data['recipient']
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
            return redirect('index')
    else:
        form = EmailForm()
    return render(request, 'send_email.html', {'form': form})

def send_sms(request):
    if request.method == 'POST':
        form = SMSForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            recipient = form.cleaned_data['recipient']
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(body=message, from_=settings.TWILIO_PHONE_NUMBER, to=recipient)
            return redirect('index')
    else:
        form = SMSForm()
    return render(request, 'send_sms.html', {'form': form})
