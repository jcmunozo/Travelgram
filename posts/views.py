"""Posts Views"""
#django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import ListView, CreateView, UpdateView

#travelgram
from travelgram.mixins import AjaxableFormMixin

#posts
from .forms import PostForm
from .models import Post

class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all published posts"""
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 2  # posts per page — raise for production (e.g. 9–12)
    context_object_name = 'posts'

class CreatePostView(LoginRequiredMixin, CreateView):
    """Create new post view"""
    template_name = 'posts/new.html'
    form_class = PostForm
    success_url  = reverse_lazy('posts:feed')

    def form_valid(self, form):
        """Set the post author from the logged in user"""
        form.instance.user = self.request.user
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add user and profile to context"""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context

class UpdatePostView(AjaxableFormMixin, LoginRequiredMixin, UpdateView):
    """Edit an existing post (owner only)"""
    template_name = 'posts/edit.html'
    ajax_partial = 'posts/_edit_form.html'
    form_class = PostForm
    context_object_name = 'post'

    def get_queryset(self):
        """Restrict editing to the logged in user's own posts"""
        return Post.objects.filter(user=self.request.user)

    def get_next_url(self):
        """Return a safe `next` URL (the page the edit was opened from)"""
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={self.request.get_host()}
        ):
            return next_url
        return None

    def get_context_data(self, **kwargs):
        """Keep the originating page available for the form"""
        context = super().get_context_data(**kwargs)
        context['next'] = self.get_next_url() or ''
        return context

    def get_success_url(self):
        """Return to the originating section (feed/profile) after editing"""
        return self.get_next_url() or reverse_lazy('posts:feed')
