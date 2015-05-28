# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import minimal.views

urlpatterns = [
    url(r'^$', minimal.views.upload),
]
