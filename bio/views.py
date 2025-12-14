from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Person, PersonClick
from django.core.serializers import serialize
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Case, When, Value, IntegerField


def home(request):
    people = Person.objects.all()[:5]
    return render(request, "home.html", {"people": people})


def bio_detail(request, slug):
    person = get_object_or_404(Person, slug=slug)

    # Record the click
    PersonClick.objects.create(person=person, viewed_at=timezone.now())

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
    period = request.GET.get("period", "day")
    end_date = timezone.now()
    start_date = end_date

    if period == "day":
        start_date = end_date - timedelta(days=1)
    elif period == "week":
        start_date = end_date - timedelta(days=7)
    elif period == "month":
        start_date = end_date - timedelta(days=30)
    # If period is 'all', no start_date filter is applied to PersonClick

    if period == "all":
        trending_people_query = (
            PersonClick.objects.values("person")
            .annotate(click_count=Count("id"))
            .order_by("-click_count")
        )
    else:
        trending_people_query = (
            PersonClick.objects.filter(viewed_at__gte=start_date)
            .values("person")
            .annotate(click_count=Count("id"))
            .order_by("-click_count")
        )

    # Get the PIDs of trending people
    trending_person_pks = [item["person"] for item in trending_people_query]

    # Fetch the actual Person objects in the order of their trending status
    preserved = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(trending_person_pks)],
        output_field=IntegerField(),
    )

    people = Person.objects.filter(pk__in=trending_person_pks).order_by(preserved)

    return render(request, "trending.html", {"people": people, "period": period})
