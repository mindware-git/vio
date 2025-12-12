from django.db import models
from django.utils import timezone


class Person(models.Model):
    """인물 정보 모델"""

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="persons/", null=True, blank=True)
    biography = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LifeEvent(models.Model):
    """인물의 생애 사건/이정표 모델"""

    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="life_events"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
