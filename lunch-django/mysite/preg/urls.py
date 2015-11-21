from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^order/$', views.order_list, name='order_list'),
    url(r'^order/detail/(?P<order_id>[0-9]+)/$', views.order_detail, name='order_detail'),
    url(r'^order/(?P<order_id>[0-9]+)/$', views.order_detail2, name='order_detail2'),
    url(r'^order/del_order/(?P<confirmation_id>[0-9]+)/$', views.del_this_order, name='del_this_order'),
    url(r'^order/edit_confirmation/(?P<order_id>[0-9]+)/$', views.edit_confirmation_this_product, name='edit_confirmation_this_product'),
    url(r'^order/confirmation/$', views.all_order, name='all_order'),
    url(r'^order/confirmation/all/$', views.all_confirmation, name='all_confirmation'),
    url(r'^order/confirmation/order/(?P<order_id>[0-9]+)/$', views.order_detail3, name='order_detail3'),
    url(r'^order/confirmation/(?P<confirmation_id>[0-9]+)/$', views.confirmation_order, name='confirmation_order'),
    url(r'^order/profile/(?P<confirmation_id>[0-9]+)/$', views.user_order_detail, name='user_order_detail'),
    url(r'^order/profile/$', views.my_profile, name='my_profile'),
    url(r'^order/profile/edit/profile$', views.edit_profile, name='edit_profile'),
    url(r'^order/profile/edit/pass$', views.edit_pass, name='edit_pass'),
    url(r'^order/new/$', views.order_new, name='order_new'),
    url(r'^login/$', 'preg.views.log_in', name ='login'),
    url(r'^logout/$', 'preg.views.logout', name = 'logout'),
    url(r'^register/$', 'preg.views.register', name = 'register'),
    
]