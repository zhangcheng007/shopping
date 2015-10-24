
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'customer.views.customer_login'),
    url(r'^check/','customer.views.check_login'),
    #url(r'^logout/','customer.views.customer_logout'),





)
