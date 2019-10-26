from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# create category model
class Category(models.Model):
	name 		= models.CharField(max_length=250, unique=True)
	slug 		= models.SlugField(max_length=250, unique=True)
	description = models.TextField(blank=True)
	icon		= models.ImageField(upload_to = 'category/', blank=True)

	class Meta:
		ordering 			= ('name',)
		verbose_name 		= 'category'
		verbose_name_plural = 'categories'
	def __str__(self):
		return '{}'.format(self.name)

	def _get_unique_slug(self):
		slug = slugify(self.name)
		unique_slug = slug
		num = 1
		while Category.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super().save(*args, **kwargs)






class ProductManager(models.Manager):
	def get_by_id(self,id):
		qs 	=	self.get_queryset().filter(id=id)
		if qs.count()==1:
			return qs.first()
		return None


class Product(models.Model):
	name 		= models.CharField(max_length=250, unique=False) #review unique attribute	
	description = models.TextField(blank=True)
	price 		= models.DecimalField(max_digits=10, decimal_places=2)
	image 		= models.ImageField(upload_to= 'product/',blank=True)
	stock 		= models.IntegerField()
	available 	= models.BooleanField(default=True)
	created 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	votes_total = models.IntegerField(default=1)
	creator 	= models.ForeignKey(User, on_delete=models.CASCADE)
	slug 		= models.SlugField(max_length=250, unique=False) #review unique attribute
	category 	= models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

	def get_abosolute_url(self):
		return "{pk}".format(pk=self.pk)

	def summary(self):
		return self.description[:100]

	class Meta:
		ordering =('votes_total',)
		verbose_name = 'product'
		verbose_name_plural = 'products'
	def __str__(self):
		return '{}'.format(self.name)

	def _get_unique_slug(self):
		slug = slugify(self.name)
		unique_slug = slug
		num = 1
		while Product.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super().save(*args, **kwargs)





