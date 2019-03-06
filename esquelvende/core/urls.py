from django.conf.urls import url

from .views import login_user, logout_user, signup_user, home, about_us, faq

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^signup/$', signup_user),
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^about-us/$', about_us),
    url(r'^faq/$', faq),
]
