from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import re
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm, UserChangeForm
from django.contrib.auth.models import User,AbstractUser
from users.models import *
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    last_name = forms.CharField(max_length=250, label='Фамилия',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(max_length=250, label='Имя',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(max_length=250, label='Login', required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=250, label='Email', required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField( label='Повторите пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    is_active = forms.BooleanField(label='Активирован ',required=False, initial=False, widget=forms.CheckboxInput(attrs={"class":"form-control"}) )
    bankid_FK = forms.ModelChoiceField(label='Введите банковский идентификационный номер (БИН)',queryset=bankbase.objects.all(),widget=forms.Select(attrs={"class": "form-control"}))
    avatar = forms.FileField(label='Фото профиля', required=False,widget=forms.FileInput(attrs={"class": "form-control"}))
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'bankid_FK',  'email', 'password1', 'password2','avatar')


class register_new_user_form(forms.ModelForm):
    last_name = forms.CharField(max_length=250, label='Фамилия',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(max_length=250, label='Имя',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(max_length=250, label='Login', required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=250, label='Email', required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField( label='Повторите пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    is_active = forms.BooleanField(label='Активирован ',required=False, initial=False, widget=forms.CheckboxInput(attrs={"class":"form-control"}) )
    bankid_FK = forms.ModelChoiceField(label='Введите банковский идентификационный номер (БИН)',queryset=bankbase.objects.all(),widget=forms.Select(attrs={"class": "form-control"}))
    avatar = forms.FileField(label='Фото профиля', required=False, widget=forms.FileInput(attrs={"class": "form-control"}))
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'bankid_FK', 'email', 'password1', 'password2', 'avatar')



class update_user_form(forms.ModelForm):
    last_name = forms.CharField(max_length=250, label='Фамилия',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(max_length=250, label='Имя',required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(max_length=250,  label='Login', required=True, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
    email = forms.EmailField(max_length=250, label='Email', required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль',required=False, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField( label='Повторите пароль',required=False, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    is_active = forms.BooleanField(label='Активирован ',required=False, initial=False, widget=forms.CheckboxInput(attrs={"class":"form-check-input"}) )
    bankid_FK = forms.ModelChoiceField(label='Введите банковский идентификационный номер (БИН)',queryset=bankbase.objects.all(),widget=forms.Select(attrs={"class": "form-control"}))
    avatar = forms.FileField(label='Фото профиля', required=False, widget=forms.FileInput(attrs={"class": "form-control"}))
    id=forms.CharField(label='',widget=forms.HiddenInput(attrs={"class":"form-control"}))
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name',  'bankid_FK', 'email', 'avatar','password1', 'password2','is_active']




class get_users_data_form(forms.ModelForm):
    last_name = forms.CharField(max_length=250, label='Фамилия', widget=forms.TextInput(attrs={"class":"form-control","readonly":"true","disabled":"true"}))
    first_name = forms.CharField(max_length=250, label='Имя',required=True, widget=forms.TextInput(attrs={"class":"form-control","readonly":"true","disabled":"true"}))
    username = forms.CharField(max_length=250,  label='Login',  widget=forms.TextInput(attrs={"class": "form-control","readonly":"true","disabled":"true"}))
    email = forms.EmailField(max_length=250, label='Email', required=True, widget=forms.EmailInput(attrs={"class": "form-control","readonly":"true","disabled":"true"}))
    old_password = forms.CharField(label='Старый пароль', required=True,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(label='Новый пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password2 = forms.CharField( label='Повторите новый пароль',required=True, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    is_active = forms.BooleanField(label='Активирован ',required=False, initial=False, widget=forms.CheckboxInput(attrs={"class":"form-check-input","readonly":"true" }) )
    bankid_FK = forms.ModelChoiceField(label='Банковский идентификационный номер (БИН)',queryset=bankbase.objects.all(),widget=forms.Select(attrs={"class": "form-control", "disabled":"disabled" }))
    #avatar = forms.FileField(label='Фото профиля', widget=forms.FileInput(attrs={"class": "form-control"}))
    id=forms.CharField(label='',widget=forms.HiddenInput(attrs={"class":"form-control","readonly":"true"}))
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name',  'bankid_FK', 'email','old_password', 'new_password1', 'new_password2','is_active']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bankid_FK','avatar']

class EditProfileForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', required=False,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Повторите пароль', required=False,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name',  'email', 'password1', 'password2', 'is_active']

class EditProfileFormWithoutPasswords(UserChangeForm):

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name',  'email',  'is_active']

class UsernameSelectForm(forms.ModelForm):
    UList=tuple((z1,f'{z2} {z3}') for z1,z2,z3 in get_user_model().objects.values_list('id', 'first_name','last_name'))
    username = forms.ChoiceField(label='Введите логин',choices=UList, widget=forms.Select(attrs={"class": "form-control"}))
    class Meta:
        model = get_user_model()
        fields = ('username',)


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = subCategory
        fields = '__all__'

class profilesIndexForm(forms.ModelForm):
    class Meta:
        model = profilesIndex
        fields = '__all__'

class categoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = '__all__'

class profilesForm(forms.ModelForm):
    class Meta:
        model = profiles
        fields = '__all__'


class userRightsForm(forms.ModelForm):
    class Meta:
        model = userRights
        fields = '__all__'



