from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'shopping.views.index',name='index'),
    url(r'^(?P<product_id>[0-9]+)/$','shopping.views.detail', name='detail'),

    url(r'^categoryToProduct/(?P<category_id>[0-9]+)/$','shopping.views.categoryToProduct', name='categoryToProduct'),





    url(r'^staff/','shopping.views.staff',name='staff'),
    url(r'^temp/','shopping.views.testTemp',name='testTemp'),

    url(r'^base/','shopping.views.testBase',name='testBase'),
    #url(r'^subase/','shopping.views.subBase',name='subBase'),

    url(r'^form/','shopping.views.form',name='form'),
    url(r'^investigate/','shopping.views.investigate',name='investigate'),




)

