from django.conf.urls import url

from .views import load_categories, categories, category, sub_a, sub_b, products

urlpatterns = [
    url(r'^load-categories/$', load_categories),
    url(r'^categories/$', categories),
    url(r'^products$', products),
    url(r'^(?P<slug_category>[\w-]+)$', category),
    url(r'^(?P<slug_category>[\w-]+)/(?P<slug_sub_a>[\w-]+)$', sub_a),
    url(r'^(?P<slug_category>[\w-]+)/(?P<slug_sub_a>[\w-]+)/(?P<slug_sub_b>[\w-]+)$', sub_b)
]
