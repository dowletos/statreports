from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.files.storage import FileSystemStorage




class RegisterView(FormView):
    template_name = 'users/users_edit.html'
    form_class = RegisterForm
    success_url = '/'
    print('ok')

    def form_valid(self, form):
        user = form.save()
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        userX=self.request.POST.get("username")

        self.request.user.username=user
        self.request.user.id=user.id
        self.request.user.is_staff=False
        self.request.user.is_superuser = False




        if self.request.method == 'POST':
            NF = register_new_user_form(self.request.POST, instance=self.request.user)
            PF = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)

            print(NF.errors)
            print(PF.errors)
            print(NF.fields)
            print(PF.fields)
            print(self.request.FILES)d
            for z in NF.data:
               print(f'NF~~~~~~{z}')

            for v in PF.data:
                print(f'PF~~~~~~{v}')

            if NF.is_valid() and PF.is_valid():
                NF.save()
                print('ooook')
                PF.save()
                print(self.request.FILES)
                print('test')
                if self.request.FILES['avatar']:
                    upload = self.request.FILES['avatar']
                    fss = FileSystemStorage()
                    file = fss.save(upload.name, upload)
                    file_url = fss.url(file)

                messages.success(self.request, f'Your account has been sent for approval!')
                return render(self.request, 'users/users_edit.html',
                              { 'PF': PF,'NF': NF, 'title': 'Добро пожаловать', 'UserSet': UserSet})
        else:
            NF = register_new_user_form()
            PF = ProfileForm(self.request.POST)

        return render(self.request, 'users/users_edit.html', { 'PF': PF, 'title': 'Добро пожаловать', 'UserSet': UserSet})






def mainpage(request):

    UserSet=View_UserSet.objects.filter(username__exact=request.user)

    return render(request, 'login.html', { 'title': 'Добро пожаловать','UserSet':UserSet})



def users_edit_2(request):
    UserSet = View_UserSet.objects.filter(username__exact=request.user)

    if request.method == 'POST':

        NF = register_new_user_form(request.POST, instance=request.user)
        print(request.user)
        PF = ProfileForm(request.POST,instance=request.user.profile)
        print(PF.errors)
        if NF.is_valid() and PF.is_valid():
            NF.save()
            print(NF.data)
            print(PF.fields)
            PF.save()
            messages.success(request, f'Your account has been sent for approval!')
            return render(request, 'users_edit.html', {'NF': NF, 'PF': PF, 'title': 'Добро пожаловать', 'UserSet': UserSet})

    else:
        NF = register_new_user_form()
        PF = ProfileForm(request.POST)
    return render(request, 'users_edit.html', {'NF': NF, 'PF': PF, 'title': 'Добро пожаловать', 'UserSet':UserSet})


def user_profile_settings(request):
    UserSet = View_UserSet.objects.filter(username__exact=request.user)

    if request.method == 'POST':
        NF = register_new_user_form(request.POST)
        if NF.is_valid():
            register_new_user_form.objects.create(NF.cleaned_data)
    else:
        NF = register_new_user_form()
    return render(request, 'profile.html', {'NF': NF, 'title': 'Добро пожаловать', 'UserSet': UserSet})


def user_login(request):

    if request.method=='POST':
        username1 = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username1, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request,'Yahooo everything is ok')
            return redirect('/')
        else:
            messages.error(request,'an error has occured')
            return redirect('/')


def user_logout(request):
    logout(request)
    return redirect('/')

