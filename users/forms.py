"""User Forms"""
#Django
from django import forms
from django.contrib.auth.models import User

#models
from .models import Profile
from .models import User

class SignupForm(forms.Form):
    """Signup form"""
    username = forms.CharField(
        min_length=4, 
        max_length=50,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Username'
        })
    )
    password = forms.CharField(
        max_length=70, 
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'password'
        })
    )
    password_confirmation = forms.CharField(
        max_length=70, 
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Confirm password'
        })
    )

    first_name = forms.CharField(
        min_length=2, 
        max_length=50,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'First Name'
        })
    )
    last_name = forms.CharField(
        min_length=2, 
        max_length=50,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Last Name'
        })
    )

    email = forms.CharField(
        min_length=6, 
        max_length=70, 
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'Email'
        })
    )

    def clean_username(self):
        """Username must be unique"""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use')
        return username

    def clean(self):
        """Verify password confirmation match"""
        data = super().clean()
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError('Passwords do not match')
        return data
    
    def save(self):
        """Create user and profile"""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()
        return user
