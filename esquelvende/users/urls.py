from django.conf.urls import url
from .views import login_view

urlpatterns = [
    #url(r'^registrar/', new_user, name='new_user'),
    url(r'^login/', login_view),
    #url(r'^salir/', logout_view, name="logout_view"),
]
