"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from myapp.views import IndexView, FormView, FormConfirView, LoginView, RegisterView, UserProfileView, \
    updateuserprofileview, EmailVerifyView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="indexpage"),
    path('form', FormView.as_view(), name="formpage"),
    path('form-confirmation', FormConfirView.as_view(), name="formconfirmationpage"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('register', RegisterView.as_view(), name="register"),
    path('user', UserProfileView.as_view(), name="userprofile"),
    path('update-user', updateuserprofileview, name="updateuserprofile"),
    path('email-verify/<uidb64>/<token>', EmailVerifyView.as_view(), name="emailverify")
# path('update-user', changepasswordview, name="updateuserprofilepassword"),
]
