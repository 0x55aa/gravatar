# coding:utf-8
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'ermiao.views.home', name='home'),
    url(r'^accounts/', include('accounts.urls')),

)
