from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('summernote/', include('django_summernote.urls')),
    path('', include('base.urls'), name="base-urls"),
]

# credit https://stackoverflow.com/questions/5517950/django-media-url-and-media-root
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)