from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Presentation(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(max_length=100)

  def __str__(self):
    return self.title


class Poll(models.Model):
  question = models.CharField(max_length=254)
  choices = ArrayField(models.CharField(max_length=254))

  published = models.BooleanField(default=False)
  ended = models.BooleanField(default=False)

  created = models.DateTimeField(auto_now_add=True)

  presentation = models.ForeignKey(Presentation, on_delete=models.SET_NULL, blank=True, null=True)

  class Meta:
    ordering = ('-created',)

  def __str__(self):
    return self.question


class Vote(models.Model):
  poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  choice = models.PositiveSmallIntegerField()

  def __str__(self):
    return f'{self.poll} - {self.user}'
