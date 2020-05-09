from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Voter
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate
from register.models import Profile
from django.contrib.auth.models import User

from muspolic.credentials import  sp_client_st, sp_clinet_id, sp_redirect_uri
# import python os
import os

#import spotipy
import spotipy
import spotipy.util as util
from spotipy.exceptions import SpotifyException

#import timezone
from django.utils import timezone

# uses generic view from django
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')

# uses generic views from django
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'


    def get_context_data(self, **kwargs):
        """
        Returns a context containing picture of
        the current muspolic creator
        """
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        #get the object of the question
        question_of_user = Question.objects.filter(id=self.kwargs['pk']).first()
        #get the creator's name of that song
        creator_question = question_of_user.creator
        # get id of the creator's song
        id_creator = User.objects.filter(username=creator_question).first()
        # send creators profile to show his picture
        context['creator'] = Profile.objects.get(user=id_creator)
        return context

# uses generic views from django
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# define function to handle votes for user, one vote per poll is allowed
def vote(request, question_id):
    """
    Verfiies if user is authenticaed and if is elegible
    to vote. Dependging on the condiion result renders the fitting output
    """
    question = get_object_or_404(Question, pk=question_id)
    # checks if user is loged in 
    if request.user.is_authenticated:
        try:
            #looks for a selected choice(song)
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            # check if the user has already voted on this poll
            has_voted = Voter.objects.filter(question=question_id).filter(voter_name=request.user.username)
            #if user haven't voted yet , it adds the voter to the qquestion objec, and add one vote to the choice
            if len(has_voted) == 0:
                #add user as voter for this album
                Voter.objects.create(question_id=question.id, voter_name=request.user.username)
                # incrment vote in one unit
                selected_choice.votes += 1
                selected_choice.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
            # if user has already voted on this poll
            else:
                #send notification about the existance of a record
                return render(request, 'polls/results.html', {
                'question': question,
                'error_message': "You can only vote once per Album.",
            })
        #returtns votes page 
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    #if user is not auth
    else:
        #sends user to home page
        return HttpResponseRedirect(reverse('pages:home_view'))

# gets album info through Spotipy, and adds a poll model for it
def new_album(request):
    """
    Using album's spotify user, given by user
    creates a poll out of the album info
    """
    #get credential needed to conect to spoty API
    os.environ['SPOTIPY_CLIENT_ID'] = sp_clinet_id
    os.environ['SPOTIPY_CLIENT_SECRET'] = sp_client_st
    os.environ['SPOTIPY_REDIRECT_URI'] = sp_redirect_uri

    # gets questions by date from newer to oldest
    latest_question_list = Question.objects.order_by('-pub_date')

    # variables required to handle Spotify API connection and permissions
    scope = 'user-library-read'
    username = 'juan'

    #generate token to use spotify API
    token = util.prompt_for_user_token(username, scope)
    #If conection whit Spotify's API is establisehd and user is auth
    if token and request.user.is_authenticated:
        #create Spotipy object to search on Spotify's API
        sp = spotipy.Spotify(auth=token)
        #search for the album given its spotify URI
        #tries to see if uri provided by user is a valid Spotify album URI
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
                #create and save question model out of the valid album spotify URI provided by user
                new_question = Question.objects.create(
                    question_text="Which is the best song from the album \"{}\" ?".format(name_of_the_album), 
                    album_name="{}".format(name_of_the_album),
                    artist_name="{}".format(album_artist),
                    album_url="{}".format(album_img),
                    creator="{}".format(request.user.username),
                    pub_date=timezone.now()
                    )
                #add songs as choices realtes to the created question above
                for add_song in album_songs:
                    Choice.objects.create(question_id=new_question.id, choice_text=add_song, votes=0)
                return HttpResponseRedirect(reverse('polls:index'))
            #there is an existing poll fro this album
            else:
                return render(request, 'polls/index.html', {
                'error_message': "There is already a Muspolic for that Album",
                'latest_question_list' : latest_question_list,
                })
        #informatino given by user is not a valid spotify album URI
        except (KeyError, SpotifyException):
            return render(request, 'polls/index.html', {
            'error_message': "That spotify URI does not exist",
            'latest_question_list' : latest_question_list,
            })
    #conection to spotify api was denied
    else:
        return render(request, 'polls/index.html', {
            'error_message': "Cannot connect to spotify at this moment, try later",
            'latest_question_list' : latest_question_list,
        })
