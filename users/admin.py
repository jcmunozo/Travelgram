"""User Admin"""
#django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # this import help us to create profile in users in dashboard
from django.contrib.auth.models import User

#users
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin"""

    list_display = ('pk', 'user', 'phone_number', 'website', 'picture')
    list_display_links = ('pk', 'user')
    list_editable = ('phone_number','website', 'picture')
    search_fields = (
        'user__email',
        'user__username',
        'user__first_name', 
        'user__last_name',
        'phone_number'
    )
    list_filter = (
        'created', 
        'modified', 
        'user__is_active', 
        'user__is_staff'
    )

    """Custom the admin dashboard"""
    fieldsets = (
        ('Profile', {
            'fields' : (
                ('user', 'picture'),
            ),
        }),
        ('Extra info', {
            'fields' : (
                ('website'),
                ('phone_number'),
                ('biography'),
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

class ProfileInline(admin.StackedInline):
    """Profile inline admin for users"""
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
    """Add profile admid to base user admin"""
    inlines = (ProfileInline,)
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff'
    )
    list_display_links = ('username','pk')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
