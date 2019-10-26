from django.shortcuts import render, redirect
from orders.models import Order
from products.models import Product
from .models import Cart

# Create your views here.


def carthome(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	context = {'cart':cart_obj}
	return render (request, 'carts/home.html', {'cart':cart_obj})

def cartupdate(request):
	product_id			= request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj 		= Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Show message to user, product is gone?")
			return redirect('/cart/')
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)

		else:
			cart_obj.products.add(product_obj) #cart_obj.products.add(id=product_id)
		request.session['cart_items'] = cart_obj.products.count()
		#for x in cart_obj.products.all():
			#print(x)
	#return redirect('/products/'+str(product_id))
		return redirect('/cart/') # or return redirect('carts:carthome')

def checkout_home(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	if cart_created or cart_obj.products.count() == 0:
		return redirect('/cart/')
	else:
		order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
	return render(request,'carts/checkout.html',{"order": order_obj})