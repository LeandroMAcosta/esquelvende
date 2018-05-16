from django.conf.urls import url

from .views import (categories, delete_product, edit_product, home,
                    list_products, product_view, publish)

urlpatterns = [
    url(r'^$', home, name='inicio'),
    url(r'^publicar/$', publish),
    url(r'^producto/(?P<product_id>\d+)/$', product_view),
    url(r'^producto/borrar/(?P<product_id>\d+)/$', delete_product),
    url(r'^producto/editar/(?P<product_id>\d+)/$', edit_product),
    url(r'^productos/$', list_products),
    url(r'^categorias/$', categories),
    url(r'^(?P<slug_category>[\w-]+)/$', categories),
    url(r'^(?P<slug_category>[\w-]+)/(?P<slug_suba>[\w-]+)/$', categories),
    url(r'^(?P<slug_category>[\w-]+)/(?P<slug_suba>[\w-]+)/(?P<slug_subb>[\w-]+)/$', categories)
]
