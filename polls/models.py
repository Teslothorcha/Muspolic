import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    album_name = models.CharField(max_length=200, default='No name for this album')
    artist_name = models.CharField(max_length=200, default='No artist for this album')
    album_url = models.CharField(max_length=2000, default='No URL for this album')
    creator = models.CharField(max_length=200, default='juan')
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Voter(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    voter_name = models.CharField(max_length=200)

    def __str__(self):
        return self.voter_name



    