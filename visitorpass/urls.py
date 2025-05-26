from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('visitor.urls')),
    path('visitor/', include('visitor.urls')),
    path('report/', include('report.urls')),
    path('admin-portal/', include('admin_portal.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
