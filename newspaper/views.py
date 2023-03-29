from django.shortcuts import render
from django.views import generic

from .models import Topic, Redactor, Newspaper


def index(request):
    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "newspaper/index.html", context=context)


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 5


class RedactorListView(generic.ListView):
    model = Redactor
    context_object_name = "redactor_list"
    template_name = "newspaper/redactor_list.html"
    paginate_by = 5


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 5
