from django.conf.urls import url
from general import views

urlpatterns = [
    url(r'^busqueda/$', views.search, name='search_views'),
    url(r'^seguimiento/$', views.Seguimiento_view, name='Seguimiento_view'),
    url(r'^dirt_count/(?P<lista>.*)/$', views.dirt_count),
    url(r'^CrearKML2/$', views.CrearKML2),
]
