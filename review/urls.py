from django.contrib import admin
from django.urls import path, include
from . import views

app_name= 'review'

urlpatterns = [
	path('accueil/', views.acceuil, name='accueil-review'),
	path('create/', views.create_review, name='create-review'),
	path('ticket/create/', views.create_ticket, name='create-ticket'),
	path('subscription/', views.subscription, name='subscription'),
	path('subscription/<int:pk>', views.unfollow, name='unfollow'),
	path('my_post/', views.view_my_post, name='view-my-post'),
]