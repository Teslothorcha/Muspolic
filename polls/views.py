from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Voter
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate

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
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user.is_authenticated:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            has_voted = Voter.objects.filter(voter_name=request.user.username)
            if len(has_voted) == 0:
                #add user as voter for this album
                Voter.objects.create(question_id=question.id, voter_name=request.user.username)
                # incrment vote in one unit
                selected_choice.votes += 1
                selected_choice.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
            else:
                return render(request, 'polls/results.html', {
                'question': question,
                'error_message': "You can only vote once per Album.",
            })
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    else:
        return HttpResponseRedirect(reverse('pages:home_view'))

def new_album(request):
    os.environ['SPOTIPY_CLIENT_ID'] = "5071577af77f4d67bf0deba899b7c7e3"
    os.environ['SPOTIPY_CLIENT_SECRET'] = "091b14181b9d45ada442ee6122dc2af7"
    os.environ['SPOTIPY_REDIRECT_URI'] = "http://127.0.0.1:8000/polls/"

    latest_question_list = Question.objects.order_by('-pub_date')[:10]

    scope = 'user-library-read'
    username = 'juan'


    token = util.prompt_for_user_token(username, scope)
    if token and request.user.is_authenticated:
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
            
            # checks if there is already a question realted to this same album 
            repited_album = Question.objects.filter(album_name=name_of_the_album)

            #if there is no question related to this album, a question will be created
            if len(repited_album) == 0:
                new_question = Question.objects.create(
                    question_text="Which is the best song from the album \"{}\" ?".format(name_of_the_album), 
                    album_name="{}".format(name_of_the_album),
                    artist_name="{}".format(album_artist),
                    album_url="{}".format(album_img),
                    creator="{}".format(request.user.username),
                    pub_date=timezone.now()
                    )

                for add_song in album_songs:
                    Choice.objects.create(question_id=new_question.id, choice_text=add_song, votes=0)
                return HttpResponseRedirect(reverse('polls:index'))
            else:
                return render(request, 'polls/index.html', {
                'error_message': "There is already a Muspolic for that Album",
                'latest_question_list' : latest_question_list,
                })

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
