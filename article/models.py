import markdown
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import AnonymousUser
from django.utils.text import slugify
from django.urls import reverse


class Article(models.Model):
    author =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    content = models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    expired = models.DateTimeField(blank=True, null=True)
    
    tags = TaggableManager(blank=True)
    views =  models.PositiveIntegerField(blank=False, default=0)

        
    def as_markdown(self) -> str:
        return markdown.markdown(self.content, safe_mode="escape", extensions=["extra"])
    
    def __str__(self):
        return self.title