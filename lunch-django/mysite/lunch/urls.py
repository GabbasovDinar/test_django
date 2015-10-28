from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<order_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<order_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^order/$', views.neworder, name='neworder'),
    url(r'^registration/$', views.newuser, name='newuser'),
]