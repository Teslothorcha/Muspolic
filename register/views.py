from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from polls.models import Question, Choice, Voter
from .models import Profile
from .forms import ProfileForm

# Create your views here.

def create_account(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/polls")
    else:
        form = UserCreationForm()
    return render(request, "register/register.html", {"form": form})

def profile_page(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    return render(request, "register/profile.html", 
                        {"name_user": request.user.username,
                        "latest_question_list": latest_question_list}
                    )

def profile_image(request, name_user):
    questions_user = Question.objects.filter(creator=name_user)
    image_message = "Image wasn't updated, try again"
    if len(questions_user) == 0:
        questions_warning = "You haven't created any Muspolics yet"
    else:
        questions_warning = None

    if request.method == "POST":
        #Get the posted form
        form = ProfileForm(request.POST, request.FILES)
      
        if form.is_valid():
            form.save()
            image_message = "image updated succesfully"
            
    else:
        MyProfileForm = Profileform()
    
    return render(request, 'register/profile.html', {
                'error_message': questions_warning,
                'image_message': image_message,
                'name_user': request.user.username,
                })