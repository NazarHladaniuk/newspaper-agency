from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Topic, Redactor, Newspaper


@login_required
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


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class RedactorListView(generic.ListView):
    model = Redactor
    context_object_name = "redactor_list"
    template_name = "newspaper/redactor_list.html"
    paginate_by = 5


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers__publisher")


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 5
