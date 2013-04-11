# coding:utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    #register
    url(r'^register/$', 'accounts.views.register'),
    #login
    url(r'^login/$', 'accounts.views.login'),
    #logout
    url(r'^logout/$', 'accounts.views.logout'),
)
