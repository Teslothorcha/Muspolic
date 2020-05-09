from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from polls.models import Question, Choice, Voter
from .models import Profile
from .forms import ProfileForm, RegisterForm

#defines function to take register form
def create_account(request):
    """
    creates new accounts
    """
    #verifies if request is POST
    if request.method == "POST":
        #gets the cutom form object
        form = RegisterForm(request.POST)
        if form.is_valid():
            #if form is valid
            #saves user 
            form.save()
            #set credential to redirect user to main polls page
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/polls")
    #sends regular form to be filled out
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form": form})

#definel conetext for porfiel page
def profile_page(request):
    """
    sends form to update profile pic, and polls created by user
    """
    #gets polls created by user
    latest_question_list = Question.objects.filter(creator=request.user.username)
    #checks i user have created polls
    if len(latest_question_list) == 0:
        latest_question_list = None
    #gets user profile object
    user_profile = Profile.objects.get(user_id=request.user.id)
    #generates an image form for user to update profile pic
    form_im = ProfileForm(instance=user_profile)
    return render(request, "register/profile.html", 
                        {"name_user": request.user.username,
                        "form": form_im,
                        "latest_question_list": latest_question_list}
                    )

#updates profile picture form user
def profile_image(request, name_user):
    """
    updates picture of user by receiving a custom format
    defined on models
    """
    #gets context to be displayed on users profile
    latest_question_list = Question.objects.filter(creator=request.user.username)
    questions_user = Question.objects.filter(creator=name_user)
    image_message = "Image wasn't updated, try again"
    #if user havent created any polls yet
    if len(questions_user) == 0:
        questions_warning = "You haven't created any Muspolics yet"
    else:
        questions_warning = None

    if request.method == "POST":
        #Get the posted form
        user_profile = Profile.objects.get(user_id=request.user.id)
        # use image form with profile of the loged user 
        form_im = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form_im.is_valid():
            # if form is valid update image
            form_im.save()
            image_message = "image updated succesfully"
    # if not a post request, render regular format to be filled out
    else:
        form_im = ProfileForm()
    
    return render(request, 'register/profile.html', {
                'error_message': questions_warning,
                "latest_question_list": latest_question_list,
                'image_message': image_message,
                'form': form_im,
                'name_user': request.user.username,
                })