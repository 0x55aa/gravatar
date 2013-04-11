# coding:utf-8
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    avatar = models.CharField(max_length=100, default="/img/avatar.png")
