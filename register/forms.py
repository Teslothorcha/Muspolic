from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm): 
    """
    Extends standar user profile 
    to add user picture
    """
  
    class Meta: 
        model = Profile 
        fields = ['user_image']

class RegisterForm(UserCreationForm):
    """
    Extends standard form to add Email
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
             ]
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

