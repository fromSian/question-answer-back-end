'''
提问model
'''
import markdown
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.text import slugify
from django.urls import reverse


class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="作者"
    )
    title = models.CharField(max_length=150, unique=True, verbose_name="标题")
    content = models.TextField(blank=True, verbose_name="内容")

    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")

    expired = models.DateTimeField(blank=True, null=True, verbose_name="过期时间")

    tags = TaggableManager(blank=True, verbose_name="标签")
    views = models.PositiveIntegerField(blank=False, default=0, verbose_name="浏览量")

    def as_markdown(self) -> str:
        return markdown.markdown(self.content, safe_mode="escape", extensions=["extra"])

    def __str__(self):
        return self.title
