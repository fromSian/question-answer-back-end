from django.db import models

from django.conf import settings
from article.models import Article


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="文章")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="作者"
    )
    content = models.TextField(verbose_name="内容")
    is_great = models.BooleanField(default=False, verbose_name="是否为优秀作答")
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.content
