from django.db import models
from users.models import User
from product.models import Product

class Business(models.Model):
	name          = models.CharField(max_length = 30)
	address		  = models.CharField(max_length = 100)
	description   = models.CharField(max_length = 100)
	mobile_number = models.CharField(max_length = 30)
	tel_number    = models.CharField(max_length = 30)
	logo          = models.FileField(upload_to ='business/logo', null = True, blank = True)
	background    = models.FileField(upload_to ='business/background', null = True, blank = True)
	email         = models.EmailField()
	owner         = models.ForeignKey(User)
	date_created  = models.DateField(auto_now_add = True)

class Business_Products(models.Model):
	business = models.ForeignKey(Business)
	product  = models.ForeignKey(Product)