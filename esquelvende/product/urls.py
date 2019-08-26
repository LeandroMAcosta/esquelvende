from django.urls import path

from .views import (delete_product, view_product, publish_product,
                    republish_product, create_favorite, upload_image)

urlpatterns = [
    path('publish/', publish_product),
    path('product/<slug>-<int:pk>/', view_product, name="product_detail"),
    path('product/<int:pk>/delete/', delete_product, name="delete_product"),
    path('product/<int:pk>/republish/', republish_product, name="republish_product"),
    path('product/<int:pk>/favorite/', create_favorite, name="create_favorite"),
    path('product/upload-image/', upload_image, name="upload_image"),
    # path('product/<int:pk>/edit/', edit_product, name="edit_product"),
]
