from django.conf.urls import url

from .views import edit_user, login_view, logout_view, new_user

urlpatterns = [
    url(r'^registrar/$', new_user),
    url(r'^login/', login_view, name='login'),
    url(r'^salir/', logout_view, name='logout'),
    url(r'^perfil/$', edit_user, name='edit_user'),
]
