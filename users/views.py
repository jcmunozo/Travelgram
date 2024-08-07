"""Users views"""
#django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import DetailView, FormView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User

#users
from .forms import SignupForm
from .models import Profile

#posts
from posts.models import Post

class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context"""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')

        return context

class SignupView(FormView):
    """Users signup view"""
    template_name = 'users/signup.html'
    redirect_authenticated_user = True
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data"""
        form.save()
        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view"""
    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):
        """Return user's profile """
        return self.request.user.profile

    def get_success_url(self):
        """Return ti user's profile"""
        username = self.object.user.username
        return reverse('users:detail', kwargs = {'username': username})

class LoginView(auth_views.LoginView):
    """Login view"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view""" 
    next_page = reverse_lazy('users:login')
