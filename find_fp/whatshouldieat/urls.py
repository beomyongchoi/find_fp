# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.WhereAreYouView.as_view(), name='whereareyou'),
    url(r'^hereiam/$', views.hereiam, name='hereiam'),
]
