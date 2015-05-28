# -*- coding: utf-8 -*-
from django.conf.urls import url
import chunked.views

urlpatterns = [
    url(r'^$', chunked.views.upload),
]
