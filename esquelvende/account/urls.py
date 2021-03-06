from django.conf.urls import url
from .views import edit_user, history, favorites, user_products

urlpatterns = [
    url(r'^account/$', edit_user, name='edit_user'),
    url(r'^account/favorites/$', favorites),
    url(r'^account/history/$', history, name='history'),
    url(r'^account/products/$', user_products, name='user_products')
]
