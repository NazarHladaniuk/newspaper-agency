from django.urls import path

from newspaper.views import (
    index,
    NewspaperListView,
    RedactorListView,
    TopicListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
]

app_name = "newspaper"
