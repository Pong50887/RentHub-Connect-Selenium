from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello, world. You are on the right track")
