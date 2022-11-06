from django.db import models


class Comment(models.Model):
    author = models.CharField(max_length=20)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255)


class Topic(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=20)
    description = description = models.CharField(max_length=255)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    likes = models.BigIntegerField(default=0)
