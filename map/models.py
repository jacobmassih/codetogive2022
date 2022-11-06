from django.db import models


class Topic(models.Model):

    TOPIC_CHOICES = (
        ("Education", "Education"),
        ("Environment", "Environment"),
        ("World-Hunger", "World-Hunger"),
        ("Democracy", "Democracy"),
        ("Public-Health", "Public-Health"),
    )

    author = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=255)
    label = models.CharField(
        max_length=255, choices=TOPIC_CHOICES, default="Education")
    likes = models.BigIntegerField(default=0)


class Comment(models.Model):
    author = models.CharField(max_length=20)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default='approved')
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, null=True, blank=True)
