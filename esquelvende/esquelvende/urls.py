from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('products.urls')),
    url(r'', include('users.urls')),
    url(r'', include('reports.urls')),
    url(r'', include('favorites.urls')),
	url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Social Auth
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
