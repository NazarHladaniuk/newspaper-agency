from django.urls import path

from newspaper.views import index

urlpatterns = [
    path("", index),
    path("hello/", index),
]