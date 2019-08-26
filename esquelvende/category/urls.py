from django.urls import path

from .views import load_categories, categories, category, sub_a, sub_b, products

urlpatterns = [
    path('load-categories/', load_categories),  # Cambiar a publish/load/categories/
    path('categories/', categories),
    path('products', products),
    path('<slug_category>', category),
    path('<slug_category>/<slug_sub_a>', sub_a),
    path('<slug_category>/<slug_sub_a>/<slug_sub_b>', sub_b),
]
