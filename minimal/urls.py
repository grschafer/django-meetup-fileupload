# -*- coding: utf-8 -*-
from django.conf.urls import url
import minimal.views

urlpatterns = [
    url(r'^$', minimal.views.upload),
]
