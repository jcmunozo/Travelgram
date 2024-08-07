"""Users urls"""
#django
from django.urls import path

#users
from . import views

urlpatterns = [

    # management
    path(
        route='login/', 
        view=views.LoginView.as_view(), 
        name='login'
    ),
    path(
        route='logout/', 
        view=views.LogoutView.as_view(), 
        name='logout'
    ),
    path(
        route='signup/', 
        view=views.SignupView.as_view(), 
        name='signup'
    ),
    path(
        route='me/profile',
        view=views.UpdateProfileView.as_view(), 
        name='update_profile'
    ),
    # post
    path(
        route='<str:username>/',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
]
