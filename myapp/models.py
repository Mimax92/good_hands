from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name =  models.CharField(max_length=200)

class Instytution(models.Model):
    TYPE = {
        (0, 'fundacja'),
        (1, 'organizacja pozarządowa'),
        (2, 'zbiórka lokalna'),
        (3, 'domyślnie fundacja'),
    }
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    type = models.PositiveSmallIntegerField(choices=TYPE)
    categories = models.ManyToManyField(Category)
class Donation(models.Model):
    quantity = models.PositiveSmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Instytution, related_name="instytution", on_delete = models.CASCADE
    user = models.ForeignKey(User, related_name="User", on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=9, blank=True)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5)
    pick_up_date = models.DateTimeField(auto_now_add=True)
    pick_up_time = models.DateTimeField(null=True)
    pick_up_comment = models.DateTimeField(null=True)
