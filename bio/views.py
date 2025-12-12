from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, "home.html")


def bio_detail(request, slug):
    return HttpResponse(f"hello {slug}")


def explore(request):
    q = request.GET.get("q", "")
    return render(request, "explore.html", {"q": q})


def trending(request):
    return render(request, "trending.html")
