from django.conf.urls import include, url
import filefield.views

urlpatterns = [
    url(r'^$', filefield.views.upload),
]
