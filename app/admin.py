from django.contrib import admin
from .models import *

# class CarImageInline(admin.TabularInline): 
#     model = CarImage
#     extra = 1 

# @admin.register(Car)
# class CarAdmin(admin.ModelAdmin):
#     list_display = ['*']
#     inlines = [CarImageInline] 

# admin.site.register(CarImage)
admin.site.register(Merchant)

