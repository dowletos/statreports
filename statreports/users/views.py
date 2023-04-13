from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth import login 
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login, logout,update_session_auth_hash
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http.request import QueryDict
from .utils import *
from django.conf import settings
from django.urls import get_resolver

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


class CurrentBar:
    def ShowCurrentPathBar(request,UserSet):
        X1 = tuple((z3, z1, z2) for z1, z2, z3 in UserSet.values_list('categoryTitle', 'subCategoryTitle', 'subCategoryLink'))
        for zz in X1:
            if (zz[0] == request.path[1:]):
                return f'{zz[1]} / {zz[2]}'
            else:
                request.session['USER_current_path']= ''


'''
USER REGISTRATION CLASS
    Via this class you could:
    1. REGISTER NEW USERS
    2. DISPLAY USER REGISTRATION TEMPLATE
'''
class RegisterView(FormView):
    template_name = 'users/users_edit.html'
    form_class = RegisterForm

    def get(self, request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        request.session['USER_current_path']=CurrentBar.ShowCurrentPathBar(request,UserSet)




        if not CheckUserRights.check_user_permissions(self,UserSet, 'users_edit'):
            return redirect(reverse('logout'))
        RF = RegisterForm()
        UF = tuple((z1, f'{z2} {z3} ({z4})') for z1, z2, z3,z4 in get_user_model().objects.values_list('id', 'first_name', 'last_name','username'))
        CF = update_user_form(auto_id='id_upd_%s')
        BF = tuple((z1, f'{z1} - {z2}') for z1, z2 in bankbase.objects.all().values_list('CODE', 'LONGNAME'))

        return render(self.request, 'users/users_edit.html',
                      {'title': 'Добро пожаловать', 'UserSet': UserSet, 'form': RF, 'UF': UF, 'CF': CF, 'BF': BF})

    def form_invalid(self, form):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        request.session['USER_current_path']=CurrentBar.ShowCurrentPathBar(request,UserSet)
        if not CheckUserRights.check_user_permissions(self, UserSet, 'users_edit'):
            return redirect(reverse('logout'))
        NF = RegisterForm(self.request.POST, instance=self.request.user)

        PF = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)

        UF = tuple(
            (z1, f'{z2} {z3}') for z1, z2, z3 in get_user_model().objects.values_list('id', 'first_name', 'last_name'))
        CF = update_user_form(auto_id='id_upd_%s')
        BF = tuple((z1, f'{z1} - {z2}') for z1, z2 in bankbase.objects.all().values_list('CODE', 'LONGNAME'))
        print(NF.errors)
        print(PF.errors)
        return render(self.request, 'users/users_edit.html',
                      {'PF': PF, 'form': form, 'UF': UF, 'CF': CF, 'BF' : BF, 'title': 'Добро пожаловать', 'UserSet': UserSet})
    def form_valid(self, form):
        print("z__")
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar( request, UserSet)

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
            NF = RegisterForm(self.request.POST, instance=self.request.user)
            PF = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
            if NF.is_valid() and PF.is_valid():
                NF.save()
                print(PF.cleaned_data)
                PF.save()
                messages.success(self.request, f'Пользователь "{self.request.user}" успешно зарегистрирован.',extra_tags='users_register')
            else:
                messages.error(self.request, f'{NF.errors}{PF.errors}', extra_tags='users_register')
            UF = tuple((z1, f'{z2} {z3}') for z1, z2, z3 in get_user_model().objects.values_list('id', 'first_name', 'last_name'))
            BF = tuple((z1, f'{z1} - {z2}') for z1, z2 in bankbase.objects.all().values_list('CODE', 'LONGNAME'))

            CF = update_user_form(auto_id='id_upd_%s')

            return render(self.request, 'users/users_edit.html', { 'PF': PF, 'form': NF,'UF': UF, 'CF': CF, 'BF': BF,'title': 'Добро пожаловать', 'UserSet': UserSet})
        else:
            NF = register_new_user_form()
            PF = ProfileForm(self.request.POST)
            print("okkkk")
        return render(self.request, 'users/users_edit.html', { 'PF': PF, 'form': NF, 'title': 'Добро пожаловать', 'UserSet': UserSet})





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

        UF = tuple((z1, f'{z2} {z3}') for z1, z2, z3 in get_user_model().objects.values_list('id', 'first_name', 'last_name'))

        user_id=request.GET.get('userid')
        if User.objects.filter(id__iexact=user_id).exists():
            datax=tuple(get_user_model().objects.filter(id__iexact=user_id).values('id','username', 'first_name', 'last_name','email','is_active'))[0]
            datax_profile=tuple(Profile.objects.filter(user_id=user_id).values('user_id','bankid_FK','avatar'))[0]
            context = {
                'is_checked' : 1,
                'id' : datax["id"],
                'username' : datax["username"],
                'first_name': datax["first_name"],
                'last_name': datax["last_name"],
                'email': datax["email"],
                'is_active':datax["is_active"],
                'bankid_FK': datax_profile["bankid_FK"],
                'avatar':datax_profile["avatar"]
            }
        else:
            context = {
                'is_checked': 0,
            }
        return JsonResponse(context, status=200)




'''
User settings management class.
only  to update user settings
--update profile info
--change password
--block user
 
'''
class UpdateUser(RegisterView):
    def post(self,request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar(request, UserSet)

        if not CheckUserRights.check_user_permissions(self,UserSet, 'users_edit'):
            return redirect(reverse('logout'))
        if request.method == "POST" and User.objects.filter(id__iexact=request.POST.get('id')).exists():
            kwargs = {'data': request.POST}
            bank_upd = {'data': request.POST, 'files': request.FILES}
            usernamex=request.POST.get('username')
            kwargs['instance'] = User.objects.get(username=usernamex)
            bank_upd['instance'] = Profile.objects.get(user_id=request.POST.get('id'))
            if request.POST.get('password1') not in (" ", ""):
                NF = EditProfileForm(**kwargs)
            else:
                NF=EditProfileFormWithoutPasswords(**kwargs)
            PF = ProfileForm(**bank_upd)
            if NF.is_valid() and PF.is_valid():
                NF.save(commit=True)



                print(NF.cleaned_data)
                NF.save()
                PF.save()
                messages.success(self.request, f'Данные пользователя "{usernamex}" успешно обновлены!', extra_tags='users_update_tag')
            else:

                messages.error(self.request, NF.errors, extra_tags='users_update_tag')
            print(NF.errors)
            print(PF.errors)
            return redirect(reverse('users_update'))
        else:
                NF = register_new_user_form()
                PF = ProfileForm(self.request.POST)
                BF = tuple((z1, f'{z1} - {z2}') for z1, z2 in bankbase.objects.all().values_list('CODE', 'LONGNAME'))
                cur_level = messages.set_level(self.request, 3)
                messages.error(self.request, NF.errors, extra_tags='error')
        return render(self.request, 'users/users_edit.html',
                          {'PF': PF, 'BF': BF, 'title': 'Добро пожаловать', 'UserSet': UserSet})


'''
Create new  and manage previous users.
 --add user

'''
class CreateUserRights(FormView):
    template_name = 'users/users_rights.html'
    form_class = RegisterForm
    success_url = '/'
    def get(self, request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar(request, UserSet)

        if not CheckUserRights.check_user_permissions(self,UserSet, 'users_edit'):
            return redirect(reverse('logout'))
        RF = RegisterForm()
        UF = tuple((z1, f'{z2} {z3}') for z1, z2, z3 in get_user_model().objects.values_list('id', 'first_name', 'last_name'))
        CF = update_user_form(auto_id='id_upd_%s')

        category_list_db = category.objects.all().values_list('categoryID', 'categoryTitle')
        profile_list_db = profilesIndex.objects.all().values_list('profileIndex_PK','profileIndexTitle')
        subCategory_list_db = subCategory.objects.all().values_list('subCategoryID', 'subCategoryTitle')
        users_list_db = get_user_model().objects.all().values_list('id', 'username')


        return render(self.request, 'users/users_rights.html',
                      {'title': 'Добро пожаловать', 'UserSet': UserSet, 'form': RF, 'UF': UF, 'CF': CF,'category_form': category_list_db,'profile_form':profile_list_db, 'subCategory_form':subCategory_list_db, 'users_form':users_list_db})

    def post(self,request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar(request, UserSet)

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


class UsersSessionSettings(FormView):
     template_name = 'users/users_settings.html'
     form_class = RegisterForm
     success_url = '/'

     def get(self, request):
         UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
         request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar(request, UserSet)


         UF = tuple((z1, f'{z2} {z3}') for z1, z2, z3 in get_user_model().objects.values_list('id', 'first_name', 'last_name'))
         CF = get_users_data_form(auto_id='id_upd_%s')
         try:
               user_id=str(request.GET.get('userid',None))
               if (user_id != 'None'):
                    if get_user_model().objects.filter(id__iexact=user_id).exists():
                           datax = tuple(get_user_model().objects.filter(id__iexact=user_id).values('id', 'username', 'first_name',
                                                                                                    'last_name', 'email',
                                                                                                    'is_active'))[0]
                           datax_profile = tuple(Profile.objects.filter(user_id=user_id).values('user_id', 'bankid_FK'))[0]
                           context = {
                               'is_checked': 1,
                               'id': datax["id"],
                               'username': datax["username"],
                               'first_name': datax["first_name"],
                               'last_name': datax["last_name"],
                               'email': datax["email"],
                               'is_active': datax["is_active"],
                               'bankid_FK': datax_profile["bankid_FK"],
                           }
                           return JsonResponse(context, status=200)
                    else:
                           context = {
                               'is_checked': 0,
                               'message': 'Sorry buddy :), try to hack me next time'
                           }
                           return JsonResponse(context, status=400)

               else:
                    return render(self.request, 'users/users_settings.html',
                             {'title': 'Добро пожаловать', 'UserSet': UserSet, 'CF': CF})

         except Exception as err:
                print(f'ERROR: {err}')
                context = {
                    'is_checked': 0,
                    'message': 'Sorry buddy :), try to hack me next time'
                }
                return render(self.request, 'users/users_settings.html',
                      {'title': 'Добро пожаловать', 'context': context, 'UserSet': UserSet, 'CF': CF})



     def post(self, request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar(request, UserSet)

        kwargs_upd={}
        kwargs_upd["data"] = {'old_password': self.request.POST.get('old_password'), 'new_password1': self.request.POST.get('new_password1'), 'new_password2': self.request.POST.get('new_password2'),'id': self.request.user.id}
        form = PasswordChangeForm(request.user, **kwargs_upd)
        print(form.errors)
        if request.method == 'POST':
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(self.request, user)
                    messages.success(self.request,'Пароль успешно обновлен!',extra_tags='success')

                    return redirect(reverse('users_session_settings'))

                else:
                    CF = PasswordChangeForm(self.request.user)
                    messages.error(self.request,form.errors,extra_tags='error')
                    return redirect(reverse('users_session_settings'))
        else:
            CF = PasswordChangeForm(self.request.user)
            messages.error(self.request,form.errors,extra_tags='error')
            return render(self.request, 'users/users_settings.html',
                          {'title': 'Добро пожаловать', 'UserSet': UserSet, 'CF': form})




class UsersMessagess(FormView):
     template_name = 'users/users_messagess.html'
     form_class = RegisterForm
     success_url = '/'

     def get(self, request):
         UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
         request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar(request, UserSet)


         UF = tuple((z1, f'{z2} {z3}') for z1, z2, z3 in get_user_model().objects.values_list('id', 'first_name', 'last_name'))
         CF = get_users_data_form(auto_id='id_upd_%s')
         try:
               user_id=str(request.GET.get('userid',None))
               if (user_id != 'None'):
                    if get_user_model().objects.filter(id__iexact=user_id).exists():
                           datax = tuple(get_user_model().objects.filter(id__iexact=user_id).values('id', 'username', 'first_name',
                                                                                                    'last_name', 'email',
                                                                                                    'is_active'))[0]
                           datax_profile = tuple(Profile.objects.filter(user_id=user_id).values('user_id', 'bankid_FK'))[0]
                           context = {
                               'is_checked': 1,
                               'id': datax["id"],
                               'username': datax["username"],
                               'first_name': datax["first_name"],
                               'last_name': datax["last_name"],
                               'email': datax["email"],
                               'is_active': datax["is_active"],
                               'bankid_FK': datax_profile["bankid_FK"],
                           }
                           return JsonResponse(context, status=200)
                    else:
                           context = {
                               'is_checked': 0,
                               'message': 'Sorry buddy :), try to hack me next time'
                           }
                           return JsonResponse(context, status=400)

               else:
                    return render(self.request, 'users/users_messagess.html',
                             {'title': 'Добро пожаловать', 'UserSet': UserSet, 'CF': CF})

         except Exception as err:
                print(f'ERROR: {err}')
                context = {
                    'is_checked': 0,
                    'message': 'Sorry buddy :), try to hack me next time'
                }
                return render(self.request, 'users/users_messagess.html',
                      {'title': 'Добро пожаловать', 'context': context, 'UserSet': UserSet, 'CF': CF})



     def post(self, request):
        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar(request, UserSet)

        kwargs_upd={}
        kwargs_upd["data"] = {'old_password': self.request.POST.get('old_password'), 'new_password1': self.request.POST.get('new_password1'), 'new_password2': self.request.POST.get('new_password2'),'id': self.request.user.id}
        form = PasswordChangeForm(request.user, **kwargs_upd)
        print(form.errors)
        if request.method == 'POST':
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(self.request, user)
                    messages.success(self.request,'Пароль успешно обновлен!',extra_tags='success')

                    return redirect(reverse('users_session_settings'))

                else:
                    CF = PasswordChangeForm(self.request.user)
                    messages.error(self.request,form.errors,extra_tags='error')
                    return redirect(reverse('users_session_settings'))
        else:
            CF = PasswordChangeForm(self.request.user)
            messages.error(self.request,form.errors,extra_tags='error')
            return render(self.request, 'users/users_settings.html',
                          {'title': 'Добро пожаловать', 'UserSet': UserSet, 'CF': form})










'''
    'GENERAL MULTICONTROLLER' CLASS
        1. EDIT/DELETE/ADD NEW ELEMENTS
        2. SORTING DATA
        3. FILTERING DATA
        4. PAGINATION OF RECORDS
'''

class CRUDController(FormView):

    CurrentMixin=None
    def __init__(self,Mixin_selector):

       self.CurrentMixin=Mixin_selector
       CRUDController.__bases__ = (FormView, Mixin_selector)

    def post(self, request):

        print(self.CurrentMixin)
        CRUDController.__bases__ = (FormView, self.CurrentMixin)

        print(self.CurrentMixin.initial_order)
        self.__dict__.update()
        for z in self.__dict__:
            print(z)

        UserSet = View_UserSet.objects.filter(username__exact=self.request.user)
        request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar(request, UserSet)

        if not CheckUserRights.check_user_permissions(self,UserSet, 'users_rights'):
            return redirect(reverse('logout'))

        datax = self.CurrentMixin().objectModel.objects.all().values_list(*self.CurrentMixin().get_query_value_list()).order_by(self.CurrentMixin().get_initial_order())
        datax_count = datax.count()
        if 'FORMSELECTOR' in self.request.POST:
                                            try:
                                                if 'search[value]' not in self.request.POST:
                                                    searchF = 0
                                                else:
                                                    searchF = self.request.POST.get('search[value]')

                                                if 'length' not in self.request.POST:
                                                    showNumber = -1
                                                else:
                                                    showNumber = int(self.request.POST.get('length'))

                                                if 'order[0][column]' not in self.request.POST:
                                                    orderColumn=-1
                                                else:
                                                    orderColumn = int(self.request.POST.get('order[0][column]'))

                                                if 'order[0][dir]' not in self.request.POST:
                                                    orderType = 'asc'
                                                else:
                                                    orderType = self.request.POST.get('order[0][dir]')

                                                if 'start' not in self.request.POST:
                                                    pageStart = 0
                                                else:
                                                    pageStart = int(self.request.POST.get('start'))

                                            except Exception as err:
                                                print(f'ERROR: {err}')

                                            z = [i for i in (datax._fields)]

                                            if (len(searchF) > 0):

                                                datax = datax.filter(*(self.CurrentMixin().get_search_parameters(searchF),)).values_list(*self.CurrentMixin().get_search_parameters_results_order())

                                            if (orderColumn != -1) and (orderColumn<=len(z)-1):
                                                    if orderType=='asc':
                                                        datax=datax.order_by(z[orderColumn])
                                                    else:
                                                        datax = datax.order_by(z[orderColumn]).reverse()

                                            if (showNumber != -1):
                                                if pageStart>=0:
                                                    datax = datax[pageStart:pageStart+showNumber]
                                                else:
                                                    datax = datax[0:showNumber]

                                            context = {
                                                'draw': self.request.POST.get('draw'),
                                                'recordsTotal': datax_count,
                                                'recordsFiltered': datax_count,
                                                'data': tuple(datax)
                                            }

                                            return JsonResponse(context, status=200)


        if ('action' in self.request.POST):

            if self.request.POST.get('action')=='delete':

                if 'id' in self.request.POST:

                    try:

                        item_id = 0
                        item_id=int(self.request.POST.get('id'))
                        if item_id>0:
                            print(self.get_delete_ID(item_id))
                            Status=self.CurrentMixin().objectModel.objects.filter(**(self.CurrentMixin().get_delete_ID(item_id))).delete()
                            MessageTXT=f'Запись № {item_id} успешно удалена!'

                        else:

                            MessageTXT = f'Попытка взлома или ошибка удаления записи № {item_id}!'
                            context = {
                                'id': item_id,
                                'action': "delete",
                                'message': MessageTXT
                            }
                            return JsonResponse(context, status=400)

                    except Exception as err:
                        print(f'ERROR: {err}')
                        MessageTXT=f'Ошибка удаления записи № {item_id}!'
                        context = {
                            'id': item_id,
                            'action': "delete",
                            'message': MessageTXT
                        }
                        if self.request.POST.get('id')=='new':
                            MessageTXT = f'Пустая записать удалена!'
                            context = {
                                'id': item_id,
                                'action': "delete",
                                'message': MessageTXT
                            }
                            return JsonResponse(context, status=200)
                        return JsonResponse(context, status=400)

                    context = {
                        'id': item_id,
                        'action': "delete",
                        'message': MessageTXT
                    }

                return JsonResponse(context, status=200)

        if (self.request.POST.get('action') == 'edit') and ('id' in self.request.POST):
                    if (self.request.POST.get('id')=='new'):

                        try:
                            print('okkkkkkkkkkkkkk')
                            item_id = 9999999


                            SF = self.CurrentMixin().objectForm(self.request.POST)
                            print(SF.errors)
                            if (len(dict(SF.errors)) > 0):
                                MessageTXT = list(SF.errors.values())[0]
                            else:
                                MessageTXT = SF.errors


                            print('zzzzzzzzzzzzz',MessageTXT)
                            if SF.is_valid():
                               SF.save()
                               MessageTXT = f'Новая запись успешно добавлена!'
                            else:
                                context = {
                                    'id': item_id,
                                    'action': "new",
                                    'message': MessageTXT
                                }
                                return JsonResponse(context, status=400)


                        except Exception as err:
                            print(f'ERROR: {err}')
                            MessageTXT = f'Ошибка добавления записи № {item_id}!'

                            context = {
                                'id': item_id,
                                'action': "new",
                                'message': MessageTXT
                            }
                            return JsonResponse(context, status=400)

                        context = {
                            'id': item_id,
                            'action': "new",
                            'message': MessageTXT
                        }


                        return JsonResponse(context, status=200)

        if (self.request.POST.get('action')=='edit'):

                        if 'id' in self.request.POST:

                            if (self.request.POST.get('id') != 'new'):

                                try:

                                    item_id = int(self.request.POST.get('id'))

                                    if item_id > 0:
                                        kwargs_upd = {'data': self.request.POST}

                                        kwargs_upd['instance'] = self.CurrentMixin().objectModel.objects.get(**self.CurrentMixin().get_pk_ID(item_id))

                                        SF = self.CurrentMixin().objectForm(**kwargs_upd)
                                        print(SF.errors)
                                        if (len(dict(SF.errors))>0):
                                            MessageTXT =list(SF.errors.values())[0]
                                        else:
                                            MessageTXT=SF.errors

                                        print(MessageTXT)
                                        if SF.is_valid():
                                           SF.save()
                                           MessageTXT= f'Запись № {item_id} успешно обновлена!'


                                        else:
                                            context = {
                                                'id': item_id,
                                                'action': "edit",
                                                'message': MessageTXT
                                            }
                                            return JsonResponse(context, status=400)


                                except Exception as err:
                                    print(f'ERROR: {err}')
                                    MessageTXT = f'Ошибка обновления записи № {item_id}!'

                                    context = {
                                            'id': item_id,
                                            'action': "edit",
                                            'message': MessageTXT
                                    }

                                    return JsonResponse(context, status=400)

                            context = {
                                'id': item_id,
                                'action': "edit",
                                'message': MessageTXT
                            }

                            return JsonResponse(context, status=200)

        context = {
            'id': "-1",
            'action': "None"
        }

        return JsonResponse(context, status=400)


'''
    'Users_categories' REFERENCE TABLE EDITTING CONTROLLER CLASS
        1. EDIT/DELETE/ADD NEW 
        2. SORTING DATA
        3. FILTERING DATA
        4. PAGINATION OF RECORDS
'''
class CategoriesManagementController(CRUDController):
    def __init__(self):
        kwargs = {}
        kwargs['Mixin_Selector'] = MyMixin_Categories
        super().__init__(MyMixin_Categories)

'''
    'ProfilesManagement' TABLE EDITTING CONTROLLER CLASS
        1. EDIT/DELETE/ADD NEW 
        2. SORTING DATA
        3. FILTERING DATA
        4. PAGINATION OF RECORDS
'''
class ProfilesManagementController(CRUDController):
    def __init__(self):
        kwargs={}
        kwargs['Mixin_Selector']=MyMixin_Profiles
        super().__init__(MyMixin_Profiles)

'''
    'ProfilesIndex' REFERENCE TABLE EDITTING CONTROLLER CLASS
        1. EDIT/DELETE/ADD NEW 
        2. SORTING DATA
        3. FILTERING DATA
        4. PAGINATION OF RECORDS
'''
class ProfileIndexManagementController(CRUDController):
    def __init__(self):
        kwargs={}
        kwargs['Mixin_Selector']=MyMixin_ProfileIndex
        super().__init__(MyMixin_ProfileIndex)



'''
    'Elements' REFERENCE TABLE EDITTING CONTROLLER CLASS
        1. EDIT/DELETE/ADD NEW 
        2. SORTING DATA
        3. FILTERING DATA
        4. PAGINATION OF RECORDS
'''
class ElementsManagementController(CRUDController):
    def __init__(self):
        kwargs={}
        kwargs['Mixin_Selector']=MyMixin_Elements
        super().__init__(MyMixin_Elements)



'''
    'UserRights' CONTROLLER CLASS
        1. EDIT/DELETE/ADD NEW 
        2. SORTING DATA
        3. FILTERING DATA
        4. PAGINATION OF RECORDS
'''
class UserRightsManagementController(CRUDController):
    def __init__(self):
        kwargs={}
        kwargs['Mixin_Selector']=MyMixin_UserRights
        super().__init__(MyMixin_UserRights)


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
            request.session['USER_name']=request.user.get_full_name()
            request.session['USER_avatar'] = f"{settings.MEDIA_URL}/{Profile.objects.filter(user__exact=str(request.user.id)).values('avatar')[0]['avatar'] or None}"
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



'''
Main page
'''
def mainpage(request):

    UserSet=View_UserSet.objects.filter(username__exact=request.user)
    request.session['USER_current_path'] = CurrentBar.ShowCurrentPathBar(request, UserSet)

    return render(request, 'login.html', { 'title': 'Добро пожаловать','UserSet':UserSet})





