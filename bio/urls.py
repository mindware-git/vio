from django.urls import path
from . import views

urlpatterns = [
    path("<slug>/", views.bio_detail, name="bio_detail"),
    path("<slug>/chat/", views.bio_chat, name="bio_chat"),
    path("<slug>/comment/", views.add_comment, name="add_comment"),
]
