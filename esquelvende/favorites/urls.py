from django.conf.urls import url

from .views import create_favorite, list_favorites

urlpatterns = [
    url(r'^favorito/(?P<product_id>[0-9]+)[/]?$', create_favorite,
        name='create-favorite'),
    url(r'^favoritos/$', list_favorites)
]
