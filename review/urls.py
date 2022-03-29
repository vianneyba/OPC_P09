from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('accueil/', views.acceuil, name='accueil-review'),
    path(
        'create/by-ticket/<int:pk>',
        views.create_review_by_ticket,
        name='create-review-by-ticket'
    ),
    path('review/create', views.create_review, name='create-review'),
    path('review/update/<int:pk>', views.update_review, name='update-review'),
    path('review/delete/<int:pk>', views.delete_review, name='delete-review'),
    path('ticket/create/', views.create_ticket, name='create-ticket'),
    path('ticket/delete/<int:pk>', views.delete_ticket, name='delete-ticket'),
    path('ticket/update/<int:pk>', views.update_ticket, name='update-ticket'),
    path('subscription/', views.subscription, name='subscription'),
    path('subscription/<int:pk>', views.unfollow, name='unfollow'),
    path('my_post/', views.view_my_post, name='view-my-post'),
]
