from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from comics.models import UserSettings

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['theme', 'font_size']