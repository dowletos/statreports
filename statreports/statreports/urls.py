"""mvp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from users.views import RegisterView
from users.views import *
from django.conf import settings
from django.conf.urls.static import static
from users.views import *


urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('',mainpage),
    path('login',user_login,name='login'),
    path('logout',user_logout,name='logout'),
    path('users_edit',RegisterView.as_view(), name='users_edit'),
    path('users_update',UpdateUser.as_view(), name='users_update'),
    path('check_usersinfo',GetUsersData.as_view(),name='check_usersinfo'),
    path('users_rights', CreateUserRights.as_view(), name='users_rights'),
    path('users_rights_elements_update', ElementsManagementController.as_view(), name='users_rights_elements_update'),
    path('users_rights_profiles', ProfileIndexManagementController.as_view(), name='users_rights_profiles'),
    path('users_rights_categories', CategoriesManagementController.as_view(), name='users_rights_categories'),
    path('users_rights_profileset_update', ProfilesManagementController.as_view(), name='users_rights_profileset_update'),
    path('users_rights_userrights_update', UserRightsManagementController.as_view(), name='users_rights_userrights_update'),
    path('users_session_settings', UsersSessionSettings.as_view(),        name='users_session_settings'),
    path('change_users_password', UserRightsManagementController.as_view(), name='change_users_password'),


]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


