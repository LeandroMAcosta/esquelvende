from django.urls import path
from .views import edit_user, HistoryList, Favorites, user_products

urlpatterns = [
    # path('', edit_user, name='edit_user'),
    path('favorites/', Favorites.as_view()),
    path('history/', HistoryList.as_view(), name='history'),
    path('products/', user_products, name='user_products')
]
