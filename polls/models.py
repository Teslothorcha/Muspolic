import datetime

from django.db import models
from django.utils import timezone


# define main  model that conatains the infor mation of the album
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    album_name = models.CharField(max_length=200, default='No name for this album')
    artist_name = models.CharField(max_length=200, default='No artist for this album')
    album_url = models.CharField(max_length=2000, default='No URL for this album')
    creator = models.CharField(max_length=200, default='juan')
    pub_date = models.DateTimeField('date published')

    # define custom standar output for object
    def __str__(self):
        """
        returns the queston_text, (main attr)
        of the Question object
        """
        return self.question_text

    def was_published_recently(self):
        """
        Returns the questions from last day
        """
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

#defines the choice model that has relation many to one with question model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    #defines custon standar output for object
    def __str__(self):
        """
        Return the name of the song (Choice)
        """
        return self.choice_text

#defines the voters model that has relation many to one with question model
class Voter(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    voter_name = models.CharField(max_length=200)

    #defines custon standar output for object
    def __str__(self):
        """
        Returns the name of the voter
        """
        return self.voter_name



    