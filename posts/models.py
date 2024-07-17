#Django
from django.db import models
from django.contrib.auth.models import User

#models
from users.models import Profile

# Create your models here.

class Post(models.Model):
    """Post model"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # another way is profile = models.ForeignKey('users.Profile', on_delete = models.CASCADE) this without import model

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='posts/photos')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} by @{}'.format(self.title, self.user.username)

