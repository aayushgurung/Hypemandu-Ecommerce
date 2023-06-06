from django.urls import path
from . import views

app_name='orders'

urlpatterns = [
    path('',views.order_create,name='order_create'),
    path('khalti/',views.khaltiRequest,name='khalti_request'),
    path('khalti-verify/',views.khaltiVerify,name='khalti_verify'),
    
]
