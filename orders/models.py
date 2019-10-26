from django.db import models
from carts.models import Cart
import string
import random
from django.db.models.signals import pre_save
from django.db.models.signals import post_save

ORDER_STATUS_CHOICES =(
	('created', 'Created'),
	('shipped', 'Shipped'),
	('paid', 'Paid'),
	('refunded', 'Refunded'),
	)


class Order(models.Model):
	order_id			= models.CharField(max_length=120, blank=True)
	#billing_profile		=
	#shipping_address	= 
	#billing_address		=	
	cart 				= models.ForeignKey(Cart, on_delete=models.CASCADE)
	status				= models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
	shipping_total		= models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
	order_total			= models.DecimalField(default= 0.00, max_digits=100, decimal_places=2)


	def __str__(self):
		return self.order_id

	def update_total(self):
		cart_total 		= self.cart.total
		shipping_total 	= self.shipping_total 
		new_order_total 	= cart_total #+ shipping_total
		self.order_total= new_order_total 
		self.save()
		return new_order_total

def random_string_generator(size=6, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id(instance):
	order_id_new 	= random_string_generator().upper()
	Klass 			= instance.__class__
	qs_exists 		= Klass.objects.filter(order_id=order_id_new).exists()
	if qs_exists:
		return unique_order_id(instance)
	return order_id_new

def pre_save_create_order_id(sender, instance,  *args, **kwargs):
	if not instance.order_id:
		instance.order_id=unique_order_id(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
	if not created:
		cart_obj	= instance
		cart_total 	= cart_obj.total 
		cart_id 	= cart_obj.id 
		qs 			= Order.objects.filter(cart__id=cart_id)
		if qs.count() == 1:
			order_obj = qs.first()
			order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created,  *args, **kwargs):
	if created:
		instance.update_total()

post_save.connect(post_save_order, sender=Order)
