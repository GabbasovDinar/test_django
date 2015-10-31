from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^order/$', views.order_list, name='order_list'),
    url(r'^order/(?P<order_id>[0-9]+)/$', views.order_detail, name='order_detail'),
    url(r'^order/new/$', views.order_new, name='order_new'),
    url(r'^login/$', 'lunch.views.log_in', name ='login'),
    url(r'^logout/$', 'lunch.views.logout'),
    url(r'^register/$', 'lunch.views.register', name = 'register'),
]