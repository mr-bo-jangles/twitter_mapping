from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import ForeignKey, CharField
from django_extensions.db.fields import UUIDField

class Country(models.Model):

    """
    Stores the attributes of Countries of the world, I have stored the Lat/Long as float to appease SQLite3
    As I don't anticipate performing anything other than lookups, this should be good enough while retaining
    compatibility.
    """

    uuid = UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    iso_alpha2 = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table='twitter_country'

class Profile(models.Model):

    uuid = UUIDField(primary_key=True)
    user = ForeignKey(User)
    twitter_name = CharField(max_length=40)