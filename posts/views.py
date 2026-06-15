"""Posts Views"""
#django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

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

class PostDetailView(LoginRequiredMixin, DetailView):
    """Return Post detail"""
    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'

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
