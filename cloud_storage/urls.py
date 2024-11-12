from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/', include('key_management.urls')),
    path("image-upload/", include("imageUpload.urls")),
    # path("image-view", include("imageViewer.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)