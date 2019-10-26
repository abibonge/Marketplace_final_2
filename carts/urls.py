from django.conf.urls import url
from . views import carthome, cartupdate, checkout_home
from django.urls import path, include

app_name='carts'
urlpatterns =[
	path('', carthome, name='carthome'),
	path('checkout_home/', checkout_home, name='checkout'),
    path('cartupdate/', cartupdate, name='cartupdate'),
]