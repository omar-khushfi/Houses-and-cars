from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


class Merchant(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password=models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# class Car(models.Model):
#     merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="cars")
#     make = models.CharField(max_length=50)
#     car_class = models.CharField(max_length=50)
#     model = models.CharField(max_length=50)
#     mileage = models.CharField(max_length=20)
#     color = models.CharField(max_length=30)
#     inside_color = models.CharField(max_length=30)
#     car_type = models.CharField(max_length=30)
#     gear_type = models.CharField(max_length=20)
#     wheel_drive = models.CharField(max_length=50)
#     seat_type = models.CharField(max_length=30)
#     year = models.PositiveIntegerField()
#     cylinder = models.PositiveIntegerField()
#     gps = models.BooleanField(default=False)
#     cd = models.BooleanField(default=False)
#     dvd = models.BooleanField(default=False)
#     rear_camera = models.BooleanField(default=False)
#     sensors = models.BooleanField(default=False)
#     sun_roof = models.BooleanField(default=False)
#     with_warranty = models.BooleanField(default=False)
#     bluetooth = models.BooleanField(default=False)
#     fuel_type = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.make} {self.model} ({self.year})"


# class CarImage(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_images")
#     image = models.ImageField(upload_to="photos/car_images/")

#     def __str__(self):
#         return f"Image for {self.car.make} {self.car.model}"











# @receiver(post_delete, sender=CarImage)
# def delete_car_image_file(sender, instance, **kwargs):
#     if instance.image:
#         if os.path.isfile(instance.image.path):
#             os.remove(instance.image.path)
            
# @receiver(post_delete, sender=Car)
# def delete_car_images_on_car_delete(sender, instance, **kwargs):
#     for image in instance.images.all():
#         if image.image and os.path.isfile(image.image.path):
#             os.remove(image.image.path)