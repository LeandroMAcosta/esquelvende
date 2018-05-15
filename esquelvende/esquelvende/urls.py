from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'', include('users.urls')),
    url(r'', include('products.urls')),
    url(r'', include('reports.urls')),
    url(r'', include('favorites.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
