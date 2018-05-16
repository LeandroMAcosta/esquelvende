from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^reportar/(?P<product_id>[0-9]+)[/]?$', views.report, name="report"),
]
