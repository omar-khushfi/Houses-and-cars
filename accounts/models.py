from datetime import datetime
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.contrib.auth.models import AbstractUser
from django.db import models



class Seller(AbstractUser):
    phone = models.CharField(max_length=30)
    age=models.CharField(max_length=3)
    image = models.ImageField(upload_to="images/seller_images/")
    def __str__(self):
      return f"{self.first_name} {self.last_name}"



class Code(models.Model):
    seller=models.OneToOneField(Seller,on_delete=models.CASCADE)
    code=models.CharField(max_length=10)
    date_create=models.DateTimeField(auto_now=True)

