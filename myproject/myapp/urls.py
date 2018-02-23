# -*- coding: utf-8 -*-
from django.conf.urls import url
from myproject.myapp.views import list,log


urlpatterns = [
    url(r'^list/$', list, name='list'),
    url(r'^log/$', log, name='log')
    #url(r'log/',views.log, name='DocumentForm')
]
