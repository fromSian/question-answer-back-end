from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    first_name = None
    last_name = None

    coins =  models.PositiveIntegerField(blank=False, default=2)

    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username
