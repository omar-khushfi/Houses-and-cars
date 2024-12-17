import datetime
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


class Seller(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password=models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    image = models.ImageField(upload_to="images/erchant_images/")
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Feature(models.Model):
	feature = models.CharField( max_length=50)
	rank = models.PositiveSmallIntegerField(default=9)

	class Meta:
			ordering = ["feature"]

	def __str__(self):
			return self.feature


###################Car#################

class Car(models.Model):
	regional_spec_choices = (
		('g', 'GCC Specs'),
		('a', 'American Specs'),
		('c', 'Canadian Specs'),
		('e', 'European Specs'),
		('j', 'Japanese Specs'),
		('k', 'Korean Specs'),
		('n', 'Chinese Specs'),
		('x', 'Other'),
	)

	fuel_type_choices = (
		('p', 'Petrol'),
		('d', 'Diesel'),
		('e', 'Electric'),
		('h', 'Hybrid'),
	)
	
	warranty_choices = (
		('y', 'Yes'),
		('n', 'No'),
		('x', 'Does not apply'),
	)
	
	car_status_options = (
		('a','Active'),
		('d','Deactive'),
		('s','Sold'),
	)
	transmission_type_choices = (
		('a', 'Automatic'),
		('m', 'Manual'),
	)

	steering_side_choices = (
		('l', 'Left Hand'),
		('r', 'Right Hand'),
	)

	doors_choices = (
		('2', '2 doors'),
		('3', '3 doors'),
		('4', '4 doors'),
		('5', '5 doors'),
		('6', '6+ doors'),
	)

	seating_choices = (
		('2', '2 Seater'),
		('4', '4 Seater'),
		('5', '5 Seater'),
		('6', '6 Seater'),
		('7', '7 Seater'),
		('8', '8 Seater'),
		('9', '9+ Seater'),
	)

	cylinders_choices = (
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('8', '8'),
		('0', '10'),
		('2', '12'),
		('u', 'Unknown'),
	)

	body_type_choices = (
		('sv', 'SUV'),
		('cp', 'Coupe'),
		('se', 'Sedan'),
		('xo', 'Crossover'),
		('ht', 'Hard Top Convertible'),
		('pt', 'Pick Up Truck'),
		('hb', 'Hatchback'),
		('st', 'Soft Top Convertible'),
		('sc', 'Sports Car'),
		('vn', 'Van'),
		('wg', 'Wagon'),
		('ut', 'Utility Truck'),
		('oc', 'Other'),
	)
	
	engine_capacity_choices = (
		('a', '0 - 499 cc'),
		('b', '500 - 999 cc'),
		('c', '1000 - 1499 cc'),
		('d', '1500 - 1999 cc'),
		('e', '2000 - 2499 cc'),
		('f', '2500 - 2999 cc'),
		('g', '3000 - 3499 cc'),
		('h', '3500 - 3999 cc'),
		('i', '4000+ cc'),
		('u', 'Unknown'),
	)

	horsepower_choices = (
		('a', '0 - 99 HP'),
		('b', '100 - 199 HP'),
		('c', '200 - 299 HP'),
		('d', '300 - 399 HP'),
		('e', '400 - 499 HP'),
		('f', '500 - 599 HP'),
		('g', '600 - 699 HP'),
		('h', '700 - 799 HP'),
		('i', '800 - 899 HP'),
		('j', '900+ HP'),
		('u', 'Unknown'),
	)

	city_choices = (
		('d', 'Damascus'),
		('h', 'Homs'),
		('a', 'Aleppo'),
		('da', 'Daraa'),
		('hm', 'Hama'),
		('dr', 'Deir-ezzour'),
		('i', 'Idlib'),
		('t', 'Tartus'),
		('l', 'Latakia'),
		('r', 'Al-Ruqqa'),
	)

	year_choice = []
	plus = 2 if datetime.now().month >= 8 else 1
	for r in range(2000, (datetime.now().year + plus)):
		year_choice.append((r,r))

    
	title = models.CharField( max_length=100)	
	make = models.CharField( max_length=100)
	model = models.CharField( max_length=100)
	trim = models.CharField( max_length=100, blank=True )
	year = models.PositiveSmallIntegerField(('year'), choices=year_choice)
	kilometers = models.PositiveIntegerField(blank=True, null=True )
	exterior_color = models.CharField( max_length=100, blank=True )
	interior_color = models.CharField( max_length=100, blank=True )
	regional_spec = models.CharField(max_length=1, choices=regional_spec_choices, blank=True, default= 'g' )
	fuel_type = models.CharField(max_length=1, choices=fuel_type_choices, default= 'petrol')
	transmission = models.CharField(max_length=1, choices=transmission_type_choices, default= 'automatic')
	body_type = models.CharField(max_length=2, choices=body_type_choices, blank=True )
	doors = models.CharField(max_length=1, choices=doors_choices, blank=True )
	seating = models.CharField(max_length=1, choices=seating_choices, blank=True )
	engine_capacity = models.CharField(max_length=1, choices=engine_capacity_choices, blank=True )
	cylinders = models.CharField(max_length=1, choices=cylinders_choices, blank=True )
	horsepower = models.CharField(max_length=1, choices=horsepower_choices, blank=True )
	steering_side = models.CharField(max_length=1, choices=steering_side_choices, blank=True, default= 'l' )
	warranty = models.CharField(max_length=1, choices=warranty_choices, blank=True)
	selling_price = models.PositiveIntegerField(blank=True, null=True)
	description = models.TextField(blank=True )
	status = models.CharField(max_length=1, choices=car_status_options, default= 'active')
	is_featured = models.BooleanField(default=False)
	slug = models.SlugField(max_length=100, default="")
	features = models.ManyToManyField(Feature)
	registration_number = models.CharField( max_length=30, blank=True )
	vin = models.CharField( max_length=100, blank=True)
	created_date = models.DateField(default=datetime.now, blank=True)
	seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
      
	class Meta:
		ordering = ('title',)

	def __str__(self):
		return self.title

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_images")
    image = models.ImageField(upload_to="images/car_images/")

    def __str__(self):
        return f"Image for {self.car.make} {self.car.model}"





@receiver(post_delete, sender=CarImage)
def delete_car_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            
@receiver(post_delete, sender=Car)
def delete_car_images_on_car_delete(sender, instance, **kwargs):
    for image in instance.images.all():
        if image.image and os.path.isfile(image.image.path):
            os.remove(image.image.path)



#################estate###################


class Estate(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)    
    location = models.CharField(max_length=255)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField() 
    floor = models.IntegerField() 
    bathrooms = models.IntegerField() 
    area = models.DecimalField(max_digits=10, decimal_places=2) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class EstateImage(models.Model):
    estate = models.ForeignKey(Estate, related_name='estate_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/estate_images')

    def __str__(self):
        return f"Image for {self.estate.title}"
    
    
    
    

    
    
@receiver(post_delete, sender=EstateImage)
def delete_estate_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(post_delete, sender=Estate)
def delete_estate_images_on_estate_delete(sender, instance, **kwargs):
    for image in instance.images.all():
        if image.image and os.path.isfile(image.image.path):
            os.remove(image.image.path)
            
            
#################################