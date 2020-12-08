from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.Form):

    username=forms.CharField(label='Username',max_length=10,min_length=5,
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(label='Email',max_length=20,min_length=5,
                            widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='Password',max_length=15,min_length=6,
                            widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',max_length=15,min_length=6,
                            widget=forms.PasswordInput(attrs={'class':'form-control'}))                        