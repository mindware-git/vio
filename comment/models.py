from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Comment(models.Model):
    """
    모든 모델을 위한 댓글 모델
    """

    # Content-object field
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        related_name="content_type_set_for_%(class)s",
        on_delete=models.CASCADE,
    )
    object_pk = models.CharField("object ID", db_index=True, max_length=64)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    user_name = models.CharField("user's name", max_length=50, blank=True)
    comment = models.TextField("comment", max_length=3000)

    # Metadata about the comment
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(
        "is public",
        default=True,
        help_text="Uncheck this box to make the comment effectively disappear from the site.",
    )
    is_removed = models.BooleanField(
        "is removed",
        default=False,
        db_index=True,
        help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.',
    )

    # 대댓글을 위한 자기 참조 필드
    parent = models.ForeignKey(
        "self",
        verbose_name="parent comment",
        blank=True,
        null=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "comments_comment"
        ordering = ("created_at",)
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return "%s: %s..." % (self.name, self.comment[:50])

    def save(self, *args, **kwargs):
        if not self.is_reply_allowed():
            raise ValueError("Reply is only allowed up to 2 levels")
        super().save(*args, **kwargs)

    @property
    def name(self):
        """댓글 작성자 이름"""
        return self.user_name or "Anonymous"

    def get_depth(self):
        """댓글의 깊이를 반환 (0: 원댓글, 1: 대댓글, 2: 대대댓글)"""
        depth = 0
        current = self
        while current.parent:
            depth += 1
            current = current.parent
        return depth

    def is_reply_allowed(self):
        """대댓글이 허용되는지 확인 (2단계까지만 허용)"""
        return self.get_depth() < 3
