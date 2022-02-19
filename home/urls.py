from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('animal', views.animal, name='animal'),
    path('digit', views.digit, name='digit')
]