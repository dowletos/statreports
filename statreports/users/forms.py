from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile
import re
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User,AbstractUser
from users.models import *


class RegisterForm(UserCreationForm):
    last_name = forms.CharField(max_length=250, label='Фамилия',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(max_length=250, label='Имя',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(max_length=250, label='Login', required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=250, label='Email', required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField( label='Повторите пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    is_active = forms.BooleanField(label='Активирован ',required=False, initial=False, widget=forms.CheckboxInput(attrs={"class":"form-control"}) )
    bankid_FK = forms.ModelChoiceField(label='Введите банковский идентификационный номер (БИН)',queryset=bankbase.objects.all(),widget=forms.Select(attrs={"class": "form-control"}))
    # avatar = forms.FileField(label='Фото профиля', widget=forms.FileInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'bankid_FK',  'email', 'password1', 'password2',)



class register_new_user_form(forms.ModelForm):
    last_name = forms.CharField(max_length=250, label='Фамилия',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(max_length=250, label='Имя',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(max_length=250, label='Login', required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=250, label='Email', required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField( label='Повторите пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    is_active = forms.BooleanField(label='Активирован ',required=False, initial=False, widget=forms.CheckboxInput(attrs={"class":"form-control"}) )
    bankid_FK = forms.ModelChoiceField(label='Введите банковский идентификационный номер (БИН)',queryset=bankbase.objects.all(),widget=forms.Select(attrs={"class": "form-control"}))
    #avatar = forms.FileField(label='Фото профиля', widget=forms.FileInput(attrs={"class": "form-control"}))


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'bankid_FK', 'email', 'password1', 'password2']




class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bankid_FK',]