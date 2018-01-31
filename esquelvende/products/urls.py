from django.conf.urls import url
from .views import publish, home, product_view, delete_product, edit_product


urlpatterns = [
    url(r'^$', home, name='inicio'),
    url(r'^publicar/$', publish),
    url(r'^producto/(?P<id>\d+)/$', product_view),
    url(r'^producto/borrar/(?P<id>\d+)/$', delete_product),
    url(r'^producto/editar/(?P<id>\d+)/$', edit_product)
]
