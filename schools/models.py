from django.db import models


class School(models.Model):
    urn = models.CharField(max_length=20, unique=True, primary_key=True)
    school_name = models.CharField(max_length=100)
    open = models.BooleanField(default=True)
    open_date = models.DateField(blank=True, null=True)
    close_date = models.DateField(blank=True, null=True)
    town = models.CharField(max_length=150, blank=True)
    postcode = models.CharField(max_length=7, blank=True)
    website = models.URLField(max_length=400, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)


