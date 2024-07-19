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
        fields = ('user', 'profile', 'title','photo')
