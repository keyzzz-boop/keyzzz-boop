from django.urls import path
from . import views
urlpatterns = [
    path('', views.class_list, name='class_list'),
    path('<int:pk>/', views.class_detail, name='class_detail'),
    path('create/', views.create_class, name='create_class'),
    path('<int:pk>/edit/', views.edit_class, name='edit_class'),
    path('<int:pk>/delete/', views.delete_class, name='delete_class'),
]
