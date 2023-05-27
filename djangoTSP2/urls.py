"""
URL configuration for djangoTSP2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path, include

import accounts.views
#from landing import views

from products.views import ProductAPIView

from customers.views import CustomerAPIView
from orders.views import OrderAPIView

#import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing/', include('landing.urls')),
    path('api/v1/productlist', ProductAPIView.as_view()),
    path('api/v1/reg', CustomerAPIView.as_view()),
    path('api/v1/orders', OrderAPIView.as_view()),
    #path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('accounts.urls'), name="home"),
    path('login/', accounts.views.login_page, name="login"),
    path('register/', accounts.views.register_page, name="register"),
    path('logout/', accounts.views.logout_user, name="logout"),
    path('user/', accounts.views.userPage, name="user-page"),
    path('update_item/', accounts.views.updateItem, name="checkout"),
    path('order_history/', accounts.views.order_history_page, name="history"),
    path('kapas/', accounts.views.kapas, name="kapas"),
    path('gloves/', accounts.views.gloves, name="gloves"),
    path('bandage/', accounts.views.bandage, name="bandage"),
    path('helmets/', accounts.views.helmets, name="helmets"),
    path('profit_page/', accounts.views.profit_page, name="profit"),
    path('popular/', accounts.views.popularity_page, name="popular"),
    path('process_order/', accounts.views.processOrder, name="process_order"),
    path('update_order/', accounts.views.update_order, name="update_order")


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
