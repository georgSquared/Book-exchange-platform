from django.db import models
from django.contrib.auth.models import User
import hashlib

class Book(models.Model):

	title = models.CharField(max_length=200, blank=True)
	image_url = models.URLField()
	author = models.CharField(max_length=200, blank=True)
	available = models.BooleanField(default=True)
	owner = models.ForeignKey(User, related_name="books", default=0)
	borrower =  models.CharField(max_length=200, blank=True, default="")
	permission = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.title
	
	class Meta:
		db_table = "Book"
		


