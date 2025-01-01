from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('classes/', include('classes.urls')),
    path('attendance/', include('attendance.urls')),
    path('assignments/', include('assignments.urls')),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
