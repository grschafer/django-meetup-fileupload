from django.conf.urls import url
import filefield.views

urlpatterns = [
    url(r'^$', filefield.views.upload),
]
