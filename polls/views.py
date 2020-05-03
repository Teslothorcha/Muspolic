from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

# import python os
import os

#import spotipy
import spotipy
import spotipy.util as util
from spotipy.exceptions import SpotifyException

#import timezone
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def new_album(request):
    os.environ['SPOTIPY_CLIENT_ID'] = "5071577af77f4d67bf0deba899b7c7e3"
    os.environ['SPOTIPY_CLIENT_SECRET'] = "091b14181b9d45ada442ee6122dc2af7"
    os.environ['SPOTIPY_REDIRECT_URI'] = "http://127.0.0.1:8000/polls/"

    scope = 'user-library-read'
    username = 'juan'

    token = util.prompt_for_user_token(username, scope)

    if token:
        latest_question_list = Question.objects.order_by('-pub_date')[:10]
        sp = spotipy.Spotify(auth=token)
        #search for the album given its spotify URI
        try:
            # set varibale to store songs from the album
            album_songs = []
            # gets the JSON of the album by its URI
            album_uri = request.POST['album_uri']
            results = sp.album_tracks(album_uri)
            songs = results['items']
            #adds songs from the album to a list
            for song_name in songs:
                album_songs.append(song_name['name'])
            
            #gets album name by its URI
            album_obj = sp.album(album_uri)
            album_artist = album_obj['artists'][0]['name']
            album_img = album_obj['images'][1]['url']
            name_of_the_album = album_obj['name']

            new_question = Question.objects.create(
                question_text="Which is the best song from the album \"{}\"".format(name_of_the_album), 
                album_name="{}".format(name_of_the_album),
                artist_name="{}".format(album_artist),
                album_url="{}".format(album_img),
                pub_date=timezone.now()
                )

            for add_song in album_songs:
                Choice.objects.create(question_id=new_question.id, choice_text=add_song, votes=0)
            return HttpResponseRedirect(reverse('polls:index'))

        except (KeyError, SpotifyException):
            return render(request, 'polls/index.html', {
            'error_message': "That spotify URI does not exist",
            'latest_question_list' : latest_question_list,
            })

    else:
        return render(request, 'polls/index.html', {
            'error_message': "Cannot connect to spotify at this moment, try later",
            'latest_question_list' : latest_question_list,
        })
