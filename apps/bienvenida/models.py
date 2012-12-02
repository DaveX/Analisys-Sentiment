from django.db import models


class usuario(models.Model):
	nombre 		= models.CharField(max_length=200)
	password	= models.CharField(max_length=200)

class tweet(models.Model):
	texto		= models.TextField(max_length=300)
	idtweet		= models.CharField(max_length=200)

