from django.conf.urls import include, url
import chunked.views

urlpatterns = [
    url(r'^$', chunked.views.upload),
]
