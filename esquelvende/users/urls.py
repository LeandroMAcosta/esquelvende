from django.conf.urls import url
from .views import login_view, new_user, logout_view, edit_user

urlpatterns = [
    url(r'^registrar/$', new_user),
    url(r'^login/', login_view, name='login'),
    url(r'^salir/', logout_view, name='logout'),
	url(r'^editar/$', edit_user),
]
