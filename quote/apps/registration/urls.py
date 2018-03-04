from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^valhalla$', views.valhalla),
    url(r'^valhalla/create$', views.add),
    url(r'^create$', views.create),
    url(r'^delete$', views.delete),
    url(r'^unwant/(?P<id>\d+)$', views.unwant),
    url(r'^valhalla/item/(?P<id>\d+)$', views.item),
    url(r'^join/(?P<id>\d+)$', views.join),
]
