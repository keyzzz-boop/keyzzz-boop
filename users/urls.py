from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.create_user, name='create_user'),
    path('<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('profile/', views.profile, name='profile'),
]
