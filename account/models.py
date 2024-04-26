from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager
from django.db import models

from django.db.models.signals import post_delete, post_init, post_save
from django.dispatch import receiver
from article.models import Article
from denounce.models import Denounce


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **other_fields):
        user = User(username=username, **other_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()
        return user

    def create_superuser(self, username, password=None, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(username, password, **other_fields)


class User(AbstractUser):

    first_name = None
    last_name = None

    coins = models.PositiveIntegerField(blank=False, default=0, verbose_name='金币数')
    times = models.PositiveIntegerField(blank=False, default=2, verbose_name='可免费发布提问次数')

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


"""
举报审核通过增加金币
"""


@receiver(post_save, sender=Denounce)
def add_coins(sender, instance, **kwargs):
    if instance.denounce_status == 1:
        user = instance.user
        user.coins = user.coins + 2
        print(user.coins)
        user.save()
