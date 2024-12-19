
from django.shortcuts import render, redirect
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
import random
import string
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from .models import *

def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits  
    code = ''.join(random.choices(characters, k=length))  
    return code



myemail='omar.khu.2004@gmail.com'



class login_view(View):
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if Seller.objects.filter(email=email).exists():
            seller = Seller.objects.get(email=email)
            
          
            if check_password(password, seller.password):
                login(request, seller)
                return redirect("/")
            else:
                messages.error(request, "كلمة المرور غير صحيحة")
                return render(request, 'login.html', {'reset': "أعد تعيين كلمة المرور"})
        else:
            messages.error(request, "المستخدم غير موجود")
            return render(request, 'login.html', {'account': "سجل حساب جديد"})
        
    def get(self, request):
        return render(request, 'login.html')

    
class signup_view(View):
    template_name = 'signup.html'
    def post(self,request):
        username=request.POST.get("username")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        age=request.POST.get("age")
        phone=request.POST.get("phone")
        photo = request.FILES.get('photo') 
        if Seller.objects.filter(email=email).exists():
            messages.error(request,"this email already exists")
        if Seller.objects.filter(username=username).exists():
            messages.error(request,"this username already exists")
            return render(request,self.template_name)
        if password1 != password2 :
            messages.error(request,"your password not equal")
            return render(request,self.template_name)
        seller=Seller.objects.create(
            email=email,
            password=make_password(password1),
            age=age,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            image = photo
            )
        if seller:
            login(request,seller)
            return redirect("/")
    def get(self,request):
        return render(request,self.template_name)
    
    
class password_code(View):
    def post(self,request):
        code_send=request.POST.get('code')
        email=request.POST.get('email')
        seller=Seller.objects.get(email=email)
        
        if Code.objects.filter(code=code_send).exists():
            code_instance = Code.objects.filter(code=code_send).first()
            
            if code_instance:
                    time_created = code_instance.date_create
                    time_elapsed = timezone.now() - time_created
                    if time_elapsed > timedelta(minutes=2):
                        messages.error(request, "The code has expired. Please request a new code.")
                        return render(request, 'password_code.html', {'time': 0,'email':email}) 
                    else:
                        return render(request,"new_password.html",{'email':email})
            else:
                code_instance=Code.objects.get(seller=seller)
                time_created = code_instance.date_create
                time_elapsed = timezone.now() - time_created
                remaining_time = timedelta(minutes=2) - time_elapsed
                messages.error(request, "The code is not valid.")
                return render(request, 'password_code.html', {'time': remaining_time.total_seconds(),'email':email})
        else :
            messages.error(request, "The code is not valid.")
             
            return render(request, 'password_code.html', {'time':0,'email':email})
              
           
    def get(self,request):
        email = request.GET.get('email')
        if Seller.objects.filter(email=email).exists():
            seller = Seller.objects.get(email=email)
            new_code = generate_random_code(8) 
            code_instance = Code.objects.filter(seller=seller).first()
            if code_instance:
                time_created = code_instance.date_create
                time_elapsed = timezone.now() - time_created
                if time_elapsed > timedelta(minutes=2):
                    messages.error(request, "The code has expired. Please request a new code.")
                    return render(request, 'password_code.html', {'time': 0,'email':email}) 
                else:
                    remaining_time = timedelta(minutes=2) - time_elapsed
                    return render(request, 'password_code.html', {'time': remaining_time.total_seconds(),'email':email})
            else:
                try:
                    messages.success(request, "A new code has been sent to your email.")
                    send_mail(
                            'Password reset code', 
                            f'Your password reset code is: {new_code}', 
                            myemail,  
                            [email],  
                            fail_silently=False,
                        )
                    code_instance = Code.objects.create(seller=seller, code=new_code, date_create=timezone.now())
                    return render(request, 'password_code.html', {'time': 120,'email':email}) 
                except:
                    messages.error(request, "The code has expired. Please request a new code.")
                    return render(request, 'password_code.html', {'time': 0,'email':email}) 

        else:
            messages.error(request, "User not found")
            return render(request, 'login.html', {'account': "Register a new account",'email':email})
        
class ResendCodeView(View):
    def get(self, request):
        email = request.GET.get('email')
        if Seller.objects.filter(email=email).exists():
            seller = Seller.objects.get(email=email)
            code_instance = Code.objects.filter(seller=seller).first()

            if code_instance:
                time_created = code_instance.date_create
                time_elapsed = timezone.now() - time_created

                if time_elapsed < timedelta(minutes=2):
                    remaining_time = timedelta(minutes=2) - time_elapsed
                    messages.info(request, "The code is still valid, please use the current code.")
                    return render(request, 'password_code.html', {
                        'time': remaining_time.total_seconds(), 
                        'email': email
                    })
                else:
                    new_code = generate_random_code(8)
                    code_instance.code = new_code
                    code_instance.date_create = timezone.now()
                    code_instance.save()
                   
                    messages.success(request, "A new code has been sent to your email.")
                    send_mail(
                        'Password reset code', 
                        f'Your password reset code is: {new_code}', 
                        myemail,  
                        [email], 
                        fail_silently=False,
                    )
                    return render(request, 'password_code.html', {'time': 120, 'email': email})
            else:
                new_code = generate_random_code(8)
                Code.objects.create(seller=seller, code=new_code, date_create=timezone.now())
                send_mail(
                        'Password reset code', 
                        f'Your password reset code is: {new_code}', 
                        myemail, 
                        [email], 
                        fail_silently=False,
                    )
                messages.success(request, "A new code has been sent to your email.")
                return render(request, 'password_code.html', {'time': 120, 'email': email})
        else:
            messages.error(request, "User does not exist.")
            return redirect(reverse('login_view'))
        
        
    
class new_password(View):
    def get(self,request):
        return render(request,"new_password.html")
    def post(self,request):
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        
        seller=Seller.objects.get(email=email)
        if password1 == password2 :
            seller.password=make_password(password1)
            seller.save()
            return redirect(reverse('login_view'))
        else:
            messages.error(request,"your password not equal")
            return render(request,"new_password.html")
        
        
        
        
        
        
        


   
    
        
class sellerEditView(View):
    template_name = 'edit_seller.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)
    
    

