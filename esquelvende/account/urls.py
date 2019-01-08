from django.conf.urls import url

from .views import edit_user, history

urlpatterns = [
    url(r'^perfil/$', edit_user, name='edit_user'),
    url(r'^history/$', history, name='history'),
]
