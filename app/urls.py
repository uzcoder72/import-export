from django.urls import path
from app.views import index, product_detail, add_product, send_email, send_sms

urlpatterns = [
    path('index/', index, name='index'),
    path('product-detail/<int:product_id>/', product_detail, name='product-detail'),
    path('add-product/', add_product, name='add-product'),
    path('send-email/', send_email, name='send-email'),
    path('send-sms/', send_sms, name='send-sms'),
]
