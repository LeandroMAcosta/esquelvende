from django.conf.urls import url

from .views import edit_user

urlpatterns = [
    url(r'^account/$', edit_user, name='edit_user'),
    url(r'^account/favorites/$', favorites),
]
