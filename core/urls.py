from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from authentication.views import UserProfile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', include('authentication.urls')),
    
    # profile section
    path('<username>/', UserProfile, name='profile')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)