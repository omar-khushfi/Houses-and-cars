from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login_view.as_view(),name="login_view"),
    path('signup/',views.signup_view.as_view(),name="signup_view"),
    
    path('reset_password/',views.password_code.as_view(),name="reset_password"),
    path('reset_password/resend_code/',views.ResendCodeView.as_view(), name='resend_code'),
    path('new_password/',views.new_password.as_view(),name="new_password")
]
