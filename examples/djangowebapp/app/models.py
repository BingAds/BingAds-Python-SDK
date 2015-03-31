"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BingAdsUser(models.Model):
    #identifier = models.CharField(max_length=40, unique=True)
    user = models.OneToOneField(User)
    refresh_token = models.CharField(max_length=200)

    # For more information about str versus unicode, see https://docs.djangoproject.com/en/1.7/intro/tutorial01/
    def __unicode__(self):              # __unicode__ on Python 2
        return self.refresh_token
    #def __str__(self):              # __str__ on Python 3
        #return self.refresh_token
    