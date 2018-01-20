from django.conf.urls import url
from .views import publish, home

urlpatterns = [
    url(r'^$', home),
    url(r'^publicar', publish),
]
