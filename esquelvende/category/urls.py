from django.conf.urls import url

from .views import tree_categories, load_sub_a

urlpatterns = [
    url(r'^tree-categories/$', tree_categories),
    url(r'^load-sub-a/$', load_sub_a)
    url(r'^load-sub-b/$', load_sub_b)
    url(r'^load-brand/$', load_brand)
]
