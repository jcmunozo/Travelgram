"""Post Forms"""

#django
from django import forms

#posts
from .models import Post

class PostForm(forms.ModelForm):
    """Post model form"""

    class Meta:
        """Form settings"""

        model = Post
        # user and profile are set on the server from request.user, never
        # trusted from the submitted form.
        fields = ('title', 'photo')
