from django.conf.urls import url

from .views import (tree_categories)

urlpatterns = [
	url(r'^tree-categories/$', tree_categories)
]
