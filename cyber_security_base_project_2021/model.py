from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=60)


class Note(models.Model):
    content = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

