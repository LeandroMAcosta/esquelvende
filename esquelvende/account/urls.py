from django.conf.urls import url
from .views import edit_user, HistoryList, Favorites, user_products

urlpatterns = [
    url(r'^account/$', edit_user, name='edit_user'),
    url(r'^account/favorites/', Favorites.as_view()),
    url(r'^account/history/$', HistoryList.as_view(), name='history'),
    url(r'^account/products/$', user_products, name='user_products')
]
