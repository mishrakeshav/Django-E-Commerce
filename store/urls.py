from django.urls import path 
from . import views

urlpatterns = [
    path('', views.store, name = 'store'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('update-cart/', views.update_cart, name = 'update_cart'),
]