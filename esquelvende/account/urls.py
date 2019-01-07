from django.conf.urls import url

from .views import edit_user

urlpatterns = [
    url(r'^perfil/$', edit_user, name='edit_user'),
]
