from .models import Linksinfo
from django.core import validators
from django import forms

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField,UserChangeForm
from django.contrib.auth.models import User
from django.forms import fields
from django.forms.widgets import PasswordInput, Widget



class punches(forms.ModelForm):
    class Meta:
        model=Linksinfo
        fields=['uid','pid']
        
class user_login(AuthenticationForm):
    username=UsernameField(max_length=20,widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password=forms.CharField(max_length=12,label='PASSWORD',widget=PasswordInput(attrs={'class':'form-control'}))




#user change form

class Edituserprofileform(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        labels={'email':'Email','first_name':'First Name','last_name':'Last Name'}


# admin profile

class EditAdminprofileform(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields='__all__'
        labels={'email':'Email'}