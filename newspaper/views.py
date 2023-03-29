from django.http import HttpResponse


def index(request):
    return HttpResponse(
        "<html>"
        "<h1>Test newspaper</h1>"
        "</html>"
    )
