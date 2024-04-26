from django.db import models
from django.conf import settings
from article.models import Article

# Create your models here.


class Denounce(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="文章")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="举报用户"
    )
    TYPE_CHOICES = [
        (0, "待审核"),
        (1, "通过"),
        (2, "失败"),
    ]
    denounce_status = models.PositiveIntegerField(
        default=0, choices=TYPE_CHOICES, verbose_name="状态"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.article.title + "--" + self.user.username
