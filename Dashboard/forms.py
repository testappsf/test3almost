from .models import Linksinfo
from django.core import validators
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import fields
from django.forms.widgets import PasswordInput, Widget



class punches(forms.ModelForm):
    class Meta:
        model=Linksinfo
        fields=['uid','pid']
        
