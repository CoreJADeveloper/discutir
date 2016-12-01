from __future__ import absolute_import
from django.contrib.auth.forms import AuthenticationForm 
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    # email = forms.CharField(label="Email", max_length=30, 
    #                            widget=forms.EmailInput(attrs={'class': 'form-control', 'name': 'email'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

