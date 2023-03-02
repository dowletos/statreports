from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.http import JsonResponse


'''
USER ACCESS RIGHTS CHECKING CLASS
    Via this class you could:
    1. Check whether current user has access to open this webpage.
    2. Check whether user could run this class/func
'''
class CheckUserRights:
    def check_user_permissions(self,permissionlist,permname):
        for uname,pname in permissionlist.values_list("username","subCategoryLink"):
            if str(uname)==str(self.request.user.username) and str(pname)==str(permname):
                return True
        return False




'''
USER REGISTRATION CLASS
    Via this class you could:
    1. REGISTER NEW USERS
    2. DISPLAY USER REGISTRATION TEMPLATE
'''
class RegisterView(FormView):
    template_name = 'users/users_edit.html'
    form_class = RegisterForm
    success_url = '/'
    def get(self, request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        if not CheckUserRights.check_user_permissions(self,UserSet, 'users_edit'):
            return redirect(reverse('logout'))
        RF = RegisterForm()
        UF = tuple((z1, f'{z2} {z3}') for z1, z2, z3 in get_user_model().objects.values_list('id', 'first_name', 'last_name'))
        CF = update_user_form(auto_id='id_upd_%s')
        return render(self.request, 'users/users_edit.html',
                      {'title': 'Добро пожаловать', 'UserSet': UserSet, 'form': RF, 'UF': UF, 'CF': CF})
    def form_valid(self, form):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        if not CheckUserRights.check_user_permissions(self,UserSet, 'users_edit'):
            return redirect(reverse('logout'))
        user_copy=self.request.user
        user = form.save()
        self.request.user.username=user
        self.request.user.id=user.id
        self.request.user.is_staff=False
        self.request.user.is_superuser = False
        if self.request.POST.get("is_active")==None:
            self.request.user.is_active = False
        if self.request.method == 'POST':
            NF = register_new_user_form(self.request.POST, instance=self.request.user)
            PF = ProfileForm(self.request.POST,  instance=self.request.user.profile)
            if NF.is_valid() and PF.is_valid():
                NF.save()
                PF.save()
                #print(self.request.FILES)
               #if self.request.FILES['avatar']:
               #     upload = self.request.FILES['avatar']
               #     fss = FileSystemStorage()
               #     file = fss.save(upload.name, upload)
               #     file_url = fss.url(file)
                cur_level=messages.set_level(self.request,2)
                messages.add_message(self.request, 2, f'Пользователь "{self.request.user}" успешно зарегистрирован', extra_tags='users_edit')
                return redirect(reverse('users_edit'))
        else:
            NF = register_new_user_form()
            PF = ProfileForm(self.request.POST)
        return render(self.request, 'users/users_edit.html', { 'PF': PF, 'title': 'Добро пожаловать', 'UserSet': UserSet})




'''
    GET USER LIST CLASS
        Via this class you could:
        1. GET A LIST OF ACTUALLY REGISTERED USERS
        2. DISPLAY DETAILS OF USER'S PROFILE
    '''
class GetUsersData(FormView):
    template_name = 'users/users_edit.html'
    form_class = RegisterForm
    success_url = '/'
    def get(self, request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        if not CheckUserRights.check_user_permissions(self,UserSet, 'users_edit'):
            return redirect(reverse('logout'))
        RF = RegisterForm()
        UF = tuple((z1, f'{z2} {z3}') for z1, z2, z3 in get_user_model().objects.values_list('id', 'first_name', 'last_name'))
        CF = update_user_form()
        user_id=request.GET.get('userid')
        if User.objects.filter(id__iexact=user_id).exists():
            datax=tuple(get_user_model().objects.filter(id__iexact=user_id).values('id','username', 'first_name', 'last_name','email','is_active'))[0]
            datax_profile=tuple(Profile.objects.filter(user_id=user_id).values('user_id','bankid_FK'))[0]
            context = {
                'is_checked' : 1,
                'id' : datax["id"],
                'username' : datax["username"],
                'first_name': datax["first_name"],
                'last_name': datax["last_name"],
                'email': datax["email"],
                'is_active':datax["is_active"],
                'bankid_FK': datax_profile["bankid_FK"]
            }
        else:
            context = {
                'is_checked': 0,
            }
        return JsonResponse(context, status=200)




'''
    Profile management class. Via this class you could create/remove/edit:
        1. User's profiles
        2. Profile types
        3. Categories
        4. Category items
'''
class UpdateUser(RegisterView):
    def post(self,request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        if not CheckUserRights.check_user_permissions(self,UserSet, 'users_edit'):
            return redirect(reverse('logout'))
        if request.method == "POST" and User.objects.filter(id__iexact=request.POST.get('id')).exists():
            kwargs = {'data': request.POST}
            bank_upd = {'data': request.POST}
            kwargs['instance'] = User.objects.get(username=request.POST.get('username'))
            bank_upd['instance'] = Profile.objects.get(user_id=request.POST.get('id'))
            NF = EditProfileForm(**kwargs)
            PF = ProfileForm(**bank_upd)
            if NF.is_valid() and PF.is_valid():
                NF.save()
                PF.save()
                cur_level = messages.set_level(self.request, 3)
                messages.add_message(self.request, 3, f'Данные пользователя "{self.request.user}" успешно обновлены.',extra_tags='users_update')
            return redirect(reverse('users_update'))
        else:
                NF = register_new_user_form()
                PF = ProfileForm(self.request.POST)
        return render(self.request, 'users/users_edit.html',
                          {'PF': PF, 'title': 'Добро пожаловать', 'UserSet': UserSet})


'''
    Profile management class. Via this class you could create/remove/edit:
        1. User's profiles
        2. Profile types
        3. Categories
        4. Category items
'''
class CreateUserRights(FormView):
    def post(self,request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        if not CheckUserRights.check_user_permissions(self,UserSet, 'users_rights'):
            return redirect(reverse('logout'))

        if request.method == "POST":
            kwargs = {'data': request.POST}
            bank_upd = {'data': request.POST}
            kwargs['instance'] = User.objects.get(username=request.POST.get('username'))
            bank_upd['instance'] = Profile.objects.get(user_id=request.POST.get('id'))
            NF = EditProfileForm(**kwargs)
            PF = ProfileForm(**bank_upd)
            if NF.is_valid() and PF.is_valid():
                NF.save()
                PF.save()
                cur_level = messages.set_level(self.request, 3)
                messages.add_message(self.request, 3, f'Данные пользователя "{self.request.user}" успешно обновлены.',extra_tags='users_update')
            return redirect(reverse('users_update'))
        else:
                NF = register_new_user_form()
                PF = ProfileForm(self.request.POST)
        return render(self.request, 'users/users_edit.html',
                          {'PF': PF, 'title': 'Добро пожаловать', 'UserSet': UserSet})










'''
    USER AUTHENTIFICATION FUNCTION
    1. CHECK USER'S EXISTANCE
    2. CREATE USER'S PROFILE
'''
def user_login(request):

    if request.method=='POST':
        username1 = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username1, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,'Неправильно введен логин или пароль. Повторите попытку!')
            return redirect('/')



'''
    LOGOUT USER FUNCTION
    1. DELETE CURRENT USER'S SESSION
    2. LOGOUT
'''
def user_logout(request):
    logout(request)
    return redirect('/')














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



