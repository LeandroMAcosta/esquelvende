from django.conf.urls import url
from .views import publish, home, product_view


urlpatterns = [
    url(r'^$', home),
    url(r'^publicar', publish),
    url(r'^producto/(?P<id>\d+)/$', product_view)
]
