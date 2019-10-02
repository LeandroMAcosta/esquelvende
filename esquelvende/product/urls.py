from django.urls import path

from .views import (delete_product, product_detail, publish_product,
                    republish_product, favorite_product, upload_product_image,
                    history_product)

urlpatterns = [
    path('publish/', publish_product),
    path('<slug>-<int:pk>/', product_detail, name="product_detail"),
    path('<int:pk>/delete/', delete_product, name="delete_product"),
    path('<int:pk>/republish/', republish_product, name="republish_product"),
    path('<int:pk>/favorite/', favorite_product, name="favorite_product"),
    path('<int:pk>/history/', history_product, name="history_product"),
    path('upload/image/', upload_product_image, name="upload_product_image"),
    # path('<int:pk>/edit/', edit_product, name="edit_product"),
]
