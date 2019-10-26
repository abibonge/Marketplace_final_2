from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from carts.models import Cart
from .models import Product, Category
from django.utils import timezone
from django import forms


class ProductListView(ListView):
	queryset	=	Product.objects.all().order_by('-votes_total')


	#def product_List_View(request): (Does the same thing as above)
			#	queryset	= Product.objects.all()
			#	context		=	{
			#			'objects_list':queryset
			#	}
			#	return render(request,"product/product_List_View.html",context)

	#def get_context_data(self, *args, **kwargs):
	#	context = super(ProductListView, self).get_context_data(*args, **kwargs)
	#	return context 
	def get_object(self, *args, **kwargs):
		request 	= self.request
		pk			= self.kwargs.get('pk')
		instance	= Product.object.get_by_id(pk)
		if instance is None:
			raise Http404('Product Does Not Exist')
		return instance

class ProductDetailView(DetailView):
	queryset	=	Product.objects.all()
	template_name	=	'products/detail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		cart_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context
			
################# Merger Starting Here ##############

@login_required(login_url="/accounts/login")
def upvote(request, product_id):
	if request.method == 'POST':
		product = get_object_or_404(Product, pk=product_id)
		product.votes_total +=1
		product.save()
		return redirect('/products/'+str(product.id))
	else:
		return redirect('/products/'+str(product.id))


@login_required(login_url="/accounts/login")
def addListing(request): #Change this to home page in product later
	if request.method == 'POST':
		if request.POST['product_name'] and request.POST['product_description'] and request.POST['product_price'] and request.FILES['product_image'] and request.POST['product_stock']:
			category = Category.objects.all() 
			product = Product()
			product.name 		= request.POST['product_name']
			product.description = request.POST['product_description']
			product.price 		=request.POST['product_price']	
			product.image 		= request.FILES['product_image']
			product.stock 		=request.POST['product_stock']	
			#product.available	=
			product.created 	=timezone.datetime.now()
			product.updated 	=timezone.datetime.now()
			product.votes_tot	= 1
			product.creator 	= request.user
			for x in category:
				if request.POST['product_category']==x.name:
					product.category=x
			product.save()
			return redirect('/products/'+str(product.id))
		else:
			return render(request, 'products/addListing.html', {'error':'Missing Required Fields'})
	else:
		return render(request, 'products/addListing.html') # Change this to home page in product later