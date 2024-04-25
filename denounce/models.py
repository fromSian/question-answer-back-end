from django.db import models
from django.conf import settings
from article.models import Article

# Create your models here.


class Denounce(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    TYPE_CHOICES = [
        (0, "待审核"),
        (1, "通过"),
        (2, "失败"),
    ]
    denounce_status = models.PositiveIntegerField(default=0, choices=TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article.title + '--' + self.user.username