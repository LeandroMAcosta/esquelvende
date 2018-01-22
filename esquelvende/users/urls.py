from django.conf.urls import url
from .views import login_view, new_user, logout_view
#from .views import test_login

urlpatterns = [
    url(r'^registrar/', new_user),
    url(r'^login/', login_view),
    url(r'^salir/', logout_view),

    #url(r'^testlogin/', test_login),
]
