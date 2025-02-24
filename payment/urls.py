from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('biling_info/', views.biling_info, name='biling_info'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', lambda request: render(request, 'payment/order_success.html'), name='order_success'),
    path('shipped_dash/', views.shipped_dash, name='shipped_dash'),
    path('not_shipped_dash/', views.not_shipped_dash, name='not_shipped_dash'),
    path('orders/<int:pk>/', views.orders, name='orders'),
]
