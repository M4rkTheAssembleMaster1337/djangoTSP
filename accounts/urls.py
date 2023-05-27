from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/', views.customer),
    path('cart/', views.cart_page, name="cart")
]
