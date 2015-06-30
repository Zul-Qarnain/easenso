from django.db import models
from users.models import User

RATE = [
	('5', '5 stars'),
	('4', '4 stars'),
	('3', '3 stars'),
	('2', '2 stars'),
	('1', '1 star'),
]

class Category(models.Model):
	name         = models.CharField(max_length = 30)
	description  = models.CharField(max_length = 100)
	date_created = models.DateField(auto_now_add = True)

class Sub_Category(models.Model):
	name         = models.CharField(max_length = 30)
	description  = models.CharField(max_length = 100)
	date_created = models.DateField(auto_now_add = True)
	category     = models.ForeignKey(Category)

class Product(models.Model):
	STATUS = [
		('B', 'Brand New'),
		('S', 'Second Hand'),
	]

	name         = models.CharField(max_length = 30)
	description  = models.CharField(max_length = 100)
	price 		   = models.DecimalField(max_digits = 7, decimal_places = 2, default=0)
	warranty     = models.DateField(null = True)
	status       = models.CharField(max_length = 1, choices = STATUS)
	owner	       = models.ForeignKey(User)
	date_created = models.DateField(auto_now_add = True)
	category     = models.ForeignKey(Sub_Category)

class User_Rate(models.Model):
	user    = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	rate    = models.CharField(max_length = 1, choices = RATE)

class VIP_Rate(models.Model):
	user    = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	rate    = models.CharField(max_length = 1, choices = RATE)

class Featured(models.Model):
	product       = models.ForeignKey(Product)
	date_featured = models.DateTimeField(auto_now_add = True)

class Product_Media(models.Model):
	media        = models.FileField(upload_to ='product/media', null = True, blank = True)
	caption      = models.CharField(max_length = 50)
	date_created = models.DateField(auto_now_add = True)

class Product_Details(models.Model):
	product = models.ForeignKey(Product)
	color   = models.CharField(max_length = 30)
	size    = models.CharField(max_length = 30)
	model   = models.CharField(max_length = 30)