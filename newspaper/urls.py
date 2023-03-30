from django.urls import path

from newspaper.views import (
    index,
    NewspaperListView,
    RedactorListView,
    TopicListView,
    NewspaperDetailView,
    RedactorDetailView,
    NewspaperCreateView,
    TopicCreateView,
    RedactorCreateView,
    TopicUpdateView,
    TopicDeleteView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    RedactorUpdateView,
    RedactorDeleteView,
    toggle_assign_to_newspapers,
)

urlpatterns = [
    path("", index, name="index"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path(
        "newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"
    ),
    path("redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
    path(
        "newspapers/create/",
        NewspaperCreateView.as_view(),
        name="newspaper-create",
    ),
    path(
        "newspapers/<int:pk>/update/",
        NewspaperUpdateView.as_view(),
        name="newspaper-update",
    ),
    path(
        "newspapers/<int:pk>/delete/",
        NewspaperDeleteView.as_view(),
        name="newspaper-delete",
    ),
    path(
        "topics/create/",
        TopicCreateView.as_view(),
        name="topic-create",
    ),
    path(
        "topics/<int:pk>/update/",
        TopicUpdateView.as_view(),
        name="topic-update",
    ),
    path(
        "topics/<int:pk>/delete/",
        TopicDeleteView.as_view(),
        name="topic-delete",
    ),
    path(
        "redactors/create/",
        RedactorCreateView.as_view(),
        name="redactor-create",
    ),
    path(
        "redactors/<int:pk>/update/",
        RedactorUpdateView.as_view(),
        name="redactor-update",
    ),
    path(
        "redactors/<int:pk>/delete/",
        RedactorDeleteView.as_view(),
        name="redactor-delete",
    ),
    path(
        "newspapers/<int:pk>/toggle-assign/",
        toggle_assign_to_newspapers,
        name="toggle-newspaper-assign",
    ),
]

app_name = "newspaper"
