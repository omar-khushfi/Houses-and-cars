from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
   path('signup/', MerchantSignUpView.as_view(), name='signup'),
    path('login/', MerchantLoginView.as_view(), name='login'),
]
