from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<OrderProductLine_id>[0-9]+)/$', views.orders, name='orders'),
    url(r'^(?P<OrderProductLine_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<OrderProductLine_id>[0-9]+)/processing/$', views.processing, name='processing'),
    url(r'^(?P<user_id>[0-9]+)/reguser/$', views.reguser, name='reguser'),
]