from django.conf.urls import url
from .views import publish, home, product_view, delete_product


urlpatterns = [
    url(r'^$', home),
    url(r'^publicar/$', publish),
    url(r'^producto/(?P<id>\d+)/$', product_view),
    url(r'^producto/borrar/(?P<id>\d+)/$', delete_product)
]
