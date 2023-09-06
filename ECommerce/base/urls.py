from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import views



urlpatterns = [
    
    path('', views.main, name='home'),
    path('product/<str:pk>/', views.product, name='product'),
    path('user/<str:pk>', views.userProfile, name='user'),
    
    
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),
    path('editProfile/', views.editProfile, name='editProfile'),
    
    path('collections/', views.collections, name='collections'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
]
