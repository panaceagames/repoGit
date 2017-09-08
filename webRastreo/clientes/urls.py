# -*- coding: utf-8 -*-
from django.conf.urls import url
from clientes import views

urlpatterns = [
    url(r'^$', views.login_view, name='vista_login'),
    url(r'^login/$', views.login_view, name='vista_login'),
    url(r'^logout/$', views.logout_view, name='vista_logout'),
    url(r'^registro/$', views.register_view, name='vista_registro'),
    url(r'^ClientesGeneral/$', views.ClientesGeneral_view, name='vista_ClientesGeneral'),
    url(r'^DatosPersonales/(?P<id_user>.*)/$', views.singleUser_view, name='vista_user'),
    url(r'^EditarDatos/(?P<id_user>.*)/$',views.edit_user_view, name='vista_edit_user'),
    url(r'^AsociarCuentas/(?P<id_user>.*)/$',views.AsociarCuentas_view, name='vista_AsociarCuentas'),
]

