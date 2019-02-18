from django.conf.urls import url

from .views import (delete_product, home, view_product, publish_product,
                    republish_product, create_favorite, search)

urlpatterns = [
    url(r'^$', home),
    url(r'^products$', search),
    url(r'^publish/$', publish_product),
    url(r'^product/(?P<product_id>\d+)/$', view_product),
    url(r'^product/(?P<product_id>\d+)/delete/$', delete_product),
    url(r'^product/(?P<product_id>\d+)/republish/$', republish_product),
    url(r'^product/(?P<product_id>\d+)/favorite/$', create_favorite)
    # url(r'^product/(?P<product_id>\d+)/edit/$', edit_product),
]
