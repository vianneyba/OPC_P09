from django.contrib import admin
from django.urls import path, include
from . import views

app_name= 'authenticate'

urlpatterns = [
	path('login/', views.login_page, name='login'),
	path('register/', views.register_page, name='register'),
	path('logout/', views.logout_page, name='logout'),
]