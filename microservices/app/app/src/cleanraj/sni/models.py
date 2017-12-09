from django.conf import settings
from django.db import models
from django import utils
import datetime


class UserProfile(models.Model):
    """
    model for storing user information for authenticated user
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key = True)
    first_name = models.TextField(default = " ")
    last_name = models.TextField(default = " ")
    image = models.ImageField(default = " ", upload_to = settings.MEDIA_ROOT)
    mobile = models.TextField(default = " ")
    address = models.TextField(default = " ")
    facebook = models.TextField(default = " ")
    def __str__(self):
    	return "{0}".format(self.user)

class location(models.Model):
    """
    Model to store location of the areas
    """

    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    garbage_pic = models.TextField(blank=True)
    
