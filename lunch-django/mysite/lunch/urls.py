from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<order_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<order_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<order_id>[0-9]+)/userorder/$', views.userorder, name='userorder'),
    
    # ex: /lunch/5/
    #url(r'^specifics/(?P<order_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /lunch/results/
    #url(r'^(?P<order_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /lunch/order/
    #url(r'^(?<order_id>[0-9]+)/MyOrder/$', views.MyOrder, name='MyOrder'),
]