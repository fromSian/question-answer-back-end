from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.signals import post_delete, post_init, post_save
from django.dispatch import receiver
from article.models import Article
from denounce.models import Denounce
class User(AbstractUser):

    first_name = None
    last_name = None

    coins =  models.PositiveIntegerField(blank=False, default=2)

    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username


'''
举报审核通过增加金币
'''
@receiver(post_save, sender=Denounce)
def low_coins(sender, instance, **kwargs):
    if instance.is_pass:
        user = instance.user
        user.coins = user.coins + 2
        user.save()