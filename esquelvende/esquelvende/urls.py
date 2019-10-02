from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include


if settings.DEBUG:
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('product/', include('product.urls')),
    path('account/', include('account.urls')),
    path('', include('category.urls')),
    path('', include('core.urls')),
    path('', include('reports.urls')),
]
