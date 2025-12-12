from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    # Fake people data for UI-only person cards
    people = [
        {"name": "Alex Kim", "role": "Technology Entrepreneur", "location": "Seoul"},
        {"name": "Mina Park", "role": "Musician", "location": "Busan"},
        {"name": "Joon Lee", "role": "Researcher", "location": "Daegu"},
    ]
    return render(request, "home.html", {"people": people})


def bio_detail(request, slug):
    return HttpResponse(f"hello {slug}")


def explore(request):
    q = request.GET.get("q", "")
    return render(request, "explore.html", {"q": q})


def trending(request):
    # period can be 'day', 'week', 'month', 'all' (UI-only)
    period = request.GET.get("period", "day")

    # fake datasets per period (UI-only)
    fake_day = [
        {"name": "Alex Kim", "role": "Entrepreneur", "location": "Seoul"},
        {"name": "Soo Jin", "role": "Actor", "location": "Incheon"},
    ]
    fake_week = [
        {"name": "Mina Park", "role": "Musician", "location": "Busan"},
        {"name": "Hyun Woo", "role": "Athlete", "location": "Gwangju"},
        {"name": "Alex Kim", "role": "Entrepreneur", "location": "Seoul"},
    ]
    fake_month = [
        {"name": "Joon Lee", "role": "Researcher", "location": "Daegu"},
        {"name": "Mina Park", "role": "Musician", "location": "Busan"},
        {"name": "Soo Jin", "role": "Actor", "location": "Incheon"},
        {"name": "Hyun Woo", "role": "Athlete", "location": "Gwangju"},
    ]
    fake_all = fake_month + fake_week

    datasets = {
        "day": fake_day,
        "week": fake_week,
        "month": fake_month,
        "all": fake_all,
    }

    people = datasets.get(period, fake_day)
    return render(request, "trending.html", {"people": people, "period": period})
