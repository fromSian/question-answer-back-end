from django.db import models
from django.conf import settings
from article.models import Article

# Create your models here.


class Denounce(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_pass = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article.title + '--' + self.user.username + '--' + str(self.is_pass)