from django.conf.urls import url

from .views import (tree_categories, categories, category, sub_a, sub_b)

urlpatterns = [
    url(r'^tree-categories/$', tree_categories),

    url(r'^categories/$', categories),
    url(r'^(?P<slug_category>[\w-]+)/$', category),
    url(r'^(?P<slug_category>[\w-]+)/(?P<slug_suba>[\w-]+)/$', sub_a),
    url(r'^(?P<slug_category>[\w-]+)/(?P<slug_suba>[\w-]+)/\
                                     (?P<slug_subb>[\w-]+)/$', sub_b)

]
