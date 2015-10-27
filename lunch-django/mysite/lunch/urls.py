from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /lunch/
    url(r'^$', views.index, name='index'),
    # ex: /lunch/5/
    url(r'^specifics/(?P<user_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /lunch/results/
    url(r'^(?P<user_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /lunch/order/
    url(r'^(?P<user_id>[0-9]+)/order/$', views.order, name='order'),
]