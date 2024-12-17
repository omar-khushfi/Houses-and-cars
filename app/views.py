from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Merchant
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
class MerchantSignUpView(View):
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

        if Merchant.objects.filter(email=email).exists():
            messages.error(request, "البريد الإلكتروني مسجل بالفعل.")
            return render(request, self.template_name)
        if password != password1:
            messages.error(request, "كلمة المرور غير متساوية")
            return render(request, self.template_name)
        Merchant.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            country=country,
            password=make_password(password) 
        )
        messages.success(request, "تم إنشاء الحساب بنجاح.")
        return redirect('login')  



class MerchantLoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            merchant = Merchant.objects.get(email=email)
            if check_password(password, merchant.password):
                login(request, merchant) 
                messages.success(request, "تم تسجيل الدخول بنجاح.")
                return redirect('home') 
            else:
                messages.error(request, "كلمة المرور غير صحيحة.")
        except Merchant.DoesNotExist:
            messages.error(request, "المستخدم غير موجود.")

        return render(request, self.template_name)