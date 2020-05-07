from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from polls.models import Question, Choice, Voter
from .models import Profile
from .forms import ProfileForm, RegisterForm

# Create your views here.

def create_account(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/polls")
    else:
        form = RegisterForm()
    return render(request, "register/register.html", {"form": form})

def profile_page(request):
    latest_question_list = Question.objects.filter(creator=request.user.username)
    if len(latest_question_list) == 0:
        latest_question_list = None
    user_profile = Profile.objects.get(user_id=request.user.id)
    form_im = ProfileForm(instance=user_profile)
    return render(request, "register/profile.html", 
                        {"name_user": request.user.username,
                        "form": form_im,
                        "latest_question_list": latest_question_list}
                    )

def profile_image(request, name_user):
    latest_question_list = Question.objects.filter(creator=request.user.username)
    questions_user = Question.objects.filter(creator=name_user)
    image_message = "Image wasn't updated, try again"
    if len(questions_user) == 0:
        questions_warning = "You haven't created any Muspolics yet"
    else:
        questions_warning = None

    if request.method == "POST":
        #Get the posted form
        user_profile = Profile.objects.get(user_id=request.user.id)
        form_im = ProfileForm(request.POST, request.FILES, instance=user_profile)
        print(form_im)
        if form_im.is_valid():
            form_im.save()
            image_message = "image updated succesfully"
            
    else:
        form_im = ProfileForm()
    
    return render(request, 'register/profile.html', {
                'error_message': questions_warning,
                "latest_question_list": latest_question_list,
                'image_message': image_message,
                'form': form_im,
                'name_user': request.user.username,
                })