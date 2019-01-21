from django.conf.urls import url

from .views import load_categories

urlpatterns = [
    url(r'^load-categories/$', load_categories),
]
