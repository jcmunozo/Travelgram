"""post urls"""

#django
from unicodedata import name
from django.urls import URLPattern, path

#models
from posts import views

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