"""Post Urls"""
#django
from django.urls import path

#posts
from . import views

urlpatterns = [
    path(
        route='', 
        view=views.PostsFeedView.as_view(), 
        name='feed'
    ),
    path(
        route='posts/new', 
        view=views.CreatePostView.as_view(), 
        name='create'
    ),
    path(
        route='post/<int:pk>/',
        view=views.PostDetailView.as_view(),
        name='detail'
    ),
]
