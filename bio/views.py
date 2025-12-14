from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Person
from django.core.serializers import serialize


def home(request):
    people = Person.objects.all()[:5]
    return render(request, "home.html", {"people": people})


def bio_detail(request, slug):
    person = get_object_or_404(Person, slug=slug)
    all_events = person.life_events.all().order_by("event_date")

    # Get a unique, sorted list of years from the events
    years = sorted(list(set(event.event_date.year for event in all_events)))

    # Determine the selected year
    try:
        selected_year = int(request.GET.get("year", years[0] if years else None))
    except (ValueError, TypeError):
        selected_year = years[0] if years else None

    # Filter events for the selected year
    life_events = (
        all_events.filter(event_date__year=selected_year) if selected_year else []
    )

    context = {
        "person": person,
        "life_events": life_events,
        "years": years,
        "selected_year": selected_year,
    }

    if request.headers.get("HX-Request"):
        return render(request, "_event_list.html", context)

    return render(request, "bio_detail.html", context)


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
