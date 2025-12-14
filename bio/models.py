from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Person(models.Model):
    """인물 정보 모델"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, blank=True)
    image = models.ImageField(upload_to="persons/", null=True, blank=True)
    biography = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if kwargs.get("raw", False):
            super().save(*args, **kwargs)
            return

        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        # Ensure slug is unique
        if Person.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            original_slug = self.slug
            counter = 2
            while Person.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)


class LifeEvent(models.Model):
    """인물의 생애 사건/이정표 모델"""

    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="life_events"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
