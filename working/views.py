from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product, Category
from django.utils import timezone
from django.views.generic.edit import CreateView
from django import forms
from carts.models import Cart




def homepage(request): 
	products = Product.objects.order_by('-votes_total')
	return render(request, 'home_page.html',{'products':products}) 