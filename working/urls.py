"""working URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from products.views import ProductListView, ProductDetailView,upvote, addListing
from carts.views import carthome



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home_page'),
    path('products/', ProductListView.as_view(), name='product_page'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='detail_page'),
    path('<int:product_id>/upvote', upvote, name='prod_upvote'),
    path('addListing', addListing, name='addListing_page'),
    path('accounts/',include('accounts.urls')),
    path('cart/',include('carts.urls', namespace= 'carts')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
