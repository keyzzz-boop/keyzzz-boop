from django.urls import path
from . import views
urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('take/<int:class_id>/', views.take_attendance, name='take_attendance'),
    path('report/<int:class_id>/', views.attendance_report, name='attendance_report'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
]
