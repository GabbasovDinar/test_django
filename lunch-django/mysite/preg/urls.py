from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^order/$', views.order_list, name='order_list'),
    url(r'^order/(?P<order_id>[0-9]+)/$', views.order_detail, name='order_detail'),
    url(r'^order/profile/(?P<order_id>[0-9]+)/$', views.user_order_detail, name='user_order_detail'),
    url(r'^order/profile/$', views.my_profile, name='my_profile'),
    url(r'^order/new/$', views.order_new, name='order_new'),
    #url(r'^info/$', views.info, name='info'),  
    url(r'^login/$', 'preg.views.log_in', name ='login'),
    url(r'^logout/$', 'preg.views.logout', name = 'logout'),
    url(r'^register/$', 'preg.views.register', name = 'register'),    
]