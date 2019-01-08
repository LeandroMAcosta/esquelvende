from django.conf.urls import url

from .views import login_user, logout_user, signup_user

urlpatterns = [
    url(r'^signup/$', signup_user),
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
]