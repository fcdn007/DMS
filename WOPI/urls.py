#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2018-2-10

@author: qi
'''
from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'WOPI'
urlpatterns = [
    url(r'^files/(?P<fileid>[^/]+)$', views.wopiGetFileInfo),
    #     url(r'^files/(?P<fileid>[^/]+)/$',views.wopiGetFileInfo),
    url(r'^files/(?P<fileid>[^/]+)/contents$', views.wopiFileContents),
    #     url(r'^files/(?P<fileid>[^/]+)/contents/$',views.wopiFileContents),
    path('xlsx/', views.xlsxV, name='xlsx')
]
