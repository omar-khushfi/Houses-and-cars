from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import check_password
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from .models import *


###########seller###############
class SellerSignUpView(View):
    template_name = 'signup.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        country = request.POST.get('country')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if Seller.objects.filter(email=email).exists():
            messages.error(request, "البريد الإلكتروني مسجل بالفعل.")
            return render(request, self.template_name)
        if password != password1:
            messages.error(request, "كلمة المرور غير متساوية")
            return render(request, self.template_name)
        Seller.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            country=country,
            password=make_password(password) 
        )
        messages.success(request, "تم إنشاء الحساب بنجاح.")
        return redirect('login')  



class SellerLoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            seller = get_object_or_404(Seller,email=email)
            if check_password(password, seller.password):
                login(request, seller) 
                messages.success(request, "تم تسجيل الدخول بنجاح.")
                return redirect('home') 
            else:
                messages.error(request, "كلمة المرور غير صحيحة.")
        except Seller.DoesNotExist:
            messages.error(request, "المستخدم غير موجود.")

        return render(request, self.template_name)
    
    
    
        
class sellerEditView(View):
    template_name = 'edit_estate.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)
    
    






##########estate#############

class EstateView(View):
    template_name = 'estate.html'

    def get(self, request,pk):
        estate=get_object_or_404(Estate,pk=pk)
        images=EstateImage.objects.get(estate=estate)
        context={
            'estate':estate,
            'images':images
        }
        return render(request, self.template_name,context)





class EstateEditView(View):
    template_name = 'edit_estate.html'

    def get(self, request, pk):
        estate = get_object_or_404(Estate, pk=pk)
        images = EstateImage.objects.filter(estate=estate) 
        context = {
            'estate': estate,
            'images': images
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        estate = get_object_or_404(Estate, pk=pk)
        images = EstateImage.objects.filter(estate=estate) 
        data = request.POST
        if "delete_image" in data:
            image_id = data.get("delete_image")
            image = get_object_or_404(EstateImage, id=image_id, estate=estate)
            image.delete()
            messages.success(request, "تم حذف الصورة بنجاح.")
            return redirect('edit_estate', pk=pk) 
        try:
            estate.title = data.get("title")
            estate.location = data.get("location")
            estate.price = data.get("price")
            estate.rooms = data.get("rooms")
            estate.floor = data.get("floor")
            estate.bathrooms = data.get("bathrooms")
            estate.area = data.get("area")
            estate.save()
            messages.success(request, "تم تحديث بيانات المنزل بنجاح.")
        except:
            messages.error(request, "حدث خطأ أثناء حفظ البيانات.")

        context = {
            'estate': estate,
            'images': images
        }
        return render(request, self.template_name, context)






##############Car###############

class CarView(View):
    template_name = 'car.html'

    def get(self, request,pk):
        car = get_object_or_404(Car, pk=pk)
        images = CarImage.objects.filter(car=car)
        context = {
            'car': car,
            'images': images,
            'selected_features': car.features.all(),  
        }
        return render(request, self.template_name, context)
    
    

class CarAddView(View):
    template_name = 'add_car.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, pk):
        data = request.POST
        seller=request.user
        features = request.POST.getlist('features') 
        try:
            car = Car.objects.create(
                title=data.get("title"),
                make=data.get("make"),
                model=data.get("model"),
                trim=data.get("trim"),
                year=data.get("year"),
                kilometers=data.get("kilometers"),
                exterior_color=data.get("exterior_color"),
                interior_color=data.get("interior_color"),
                regional_spec=data.get("regional_spec"),
                fuel_type=data.get("fuel_type"),
                transmission=data.get("transmission"),
                body_type=data.get("body_type"),
                doors=data.get("doors"),
                seating=data.get("seating"),
                engine_capacity=data.get("engine_capacity"),
                cylinders=data.get("cylinders"),
                horsepower=data.get("horsepower"),
                steering_side=data.get("steering_side"),
                warranty=data.get("warranty"),
                selling_price=data.get("selling_price"),
                description=data.get("description"),
                status=data.get("status"),
                is_featured=bool(data.get("is_featured")),
                registration_number=data.get("registration_number"),
                vin=data.get("vin"),
                seller=seller
            )
            car.features.set(features)
            images = request.FILES.getlist('images')
            for image in images:
                CarImage.objects.create(car=car, image=image)
            messages.success(request, "تم اضافة  السيارة بنجاح.")
        except:
            messages.error(request, "فشل  اضافة السيارة.")

        return redirect('edit_car', pk=pk)
    
    
    
    
class CarEditView(View):
    template_name = 'edit_car.html'

    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        images = CarImage.objects.filter(car=car)
        features = Feature.objects.all()  
        context = {
            'car': car,
            'images': images,
            'features': features,
            'selected_features': car.features.all(),  
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        data = request.POST

        if "delete_image" in data:
            image_id = data.get("delete_image")
            image = get_object_or_404(CarImage, id=image_id, car=car)
            image.delete()
            messages.success(request, "تم حذف الصورة بنجاح.")
            return redirect('edit_car', pk=pk)

        try:
            car.title = data.get("title")
            car.make = data.get("make")
            car.model = data.get("model")
            car.trim = data.get("trim")
            car.year = data.get("year")
            car.kilometers = data.get("kilometers")
            car.exterior_color = data.get("exterior_color")
            car.interior_color = data.get("interior_color")
            car.regional_spec = data.get("regional_spec")
            car.fuel_type = data.get("fuel_type")
            car.transmission = data.get("transmission")
            car.body_type = data.get("body_type")
            car.doors = data.get("doors")
            car.seating = data.get("seating")
            car.engine_capacity = data.get("engine_capacity")
            car.cylinders = data.get("cylinders")
            car.horsepower = data.get("horsepower")
            car.steering_side = data.get("steering_side")
            car.warranty = data.get("warranty")
            car.selling_price = data.get("selling_price")
            car.description = data.get("description")
            car.status = data.get("status")
            car.is_featured = bool(data.get("is_featured"))
            car.registration_number = data.get("registration_number")
            car.vin = data.get("vin")
            car.save()
            
            feature_ids = request.POST.getlist("features") 
            car.features.set(feature_ids)  
            
            if request.FILES.getlist("images"):
                for image in request.FILES.getlist("images"):
                    CarImage.objects.create(car=car, image=image)

            messages.success(request, "تم تحديث بيانات السيارة بنجاح.")
        except :
            messages.error(request, "فشل في تحديث بيانات السيارة.")
        return redirect('edit_car', pk=pk)


