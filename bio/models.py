from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Person(models.Model):
    """인물 정보 모델"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, blank=True)
    image = models.ImageField(upload_to="persons/", null=True, blank=True)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    occupation = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="쉼표로 구분된 직업 목록 (예: 코미디언,방송인,유튜버)",
    )
    nationality = models.CharField(max_length=100, null=True, blank=True)
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


class PersonClick(models.Model):
    """인물 상세 페이지 클릭 기록 모델"""

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="clicks")
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["person", "viewed_at"]),
        ]
        ordering = ["-viewed_at"]


class Evidence(models.Model):
    """생애 사건/이정표의 증빙 자료 모델"""

    EVIDENCE_TYPE_CHOICES = [
        ("text", "텍스트"),
        ("link", "링크"),
        ("image", "이미지"),
        ("video", "영상"),
    ]

    life_event = models.ForeignKey(
        LifeEvent, on_delete=models.CASCADE, related_name="evidences"
    )
    evidence_type = models.CharField(max_length=10, choices=EVIDENCE_TYPE_CHOICES)
    text_content = models.TextField(blank=True, null=True)
    link_url = models.URLField(blank=True, null=True)
    image_file = models.ImageField(upload_to="evidences/images/", blank=True, null=True)
    video_file = models.FileField(upload_to="evidences/videos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.life_event.title} - {self.get_evidence_type_display()}"
