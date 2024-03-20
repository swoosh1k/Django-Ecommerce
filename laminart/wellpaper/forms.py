from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User




class UserLogin(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Username'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password'}))

    class Meta:
        model = User
        fields  = ['username', 'password',]


class UserRegistretion(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password again'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username','email',  'password1', 'password2')

