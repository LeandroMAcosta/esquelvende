from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'', include('product.urls')),
    url(r'', include('category.urls')),
    url(r'', include('account.urls')),
    url(r'', include('core.urls')),
    url(r'', include('reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
