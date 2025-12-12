from django.urls import path
from . import views

urlpatterns = [
    path("", views.bio_detail, name="bio_detail"),
]
