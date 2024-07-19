"""Post Admin"""
#django
from django.contrib import admin

#posts
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin"""

    list_display = ('pk', 'user', 'profile', 'title', 'photo')
    list_display_links = ('pk', 'user')
    list_editable = ('title', 'photo')
    search_fields = (
        'user__username'
        'title',
    )
    list_filter = (
        'created', 
        'modified'
    )

    """Custom the admin dashboard"""
    fieldsets = (
        ('Profile', {
            'fields' : (
                ('user', 'profile', 'title'),
            ),
        }),
        ('media', {
            'fields' : (
                ('photo',),
            ),
        }),
        ('Metadata', {
            'classes' : ('collapse',),
            'fields' : (
                ('created', 'modified'),
            )
        })
    )
    """Readonly is mandatory for Metadata fieldsets"""
    readonly_fields = ('created', 'modified')


