from django.conf.urls import url
from .views import create_favorite

urlpatterns = [
	url(r'^favorito/nuevo/(?P<product_id>[0-9]+)[/]?$', create_favorite, name='create-favorite'),
]