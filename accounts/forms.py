"""
Forms for user authentication and profile management.
"""

# Import necessary modules and functions from Django
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class SignupForm(UserCreationForm):
    """
    Form for user sign-up. Inherits from Django's UserCreationForm.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs=\
                               {'class': 'form-control', 'placeholder': 'Username'}),
        error_messages={'unique': 'A user with that username already exists.'}
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs=\
                                   {'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs=\
                               {'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )

    class Meta:
        """
        Metadata for the form.
        Specifies the model and the fields to be included in the form.
        """
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
        )

    def clean_username(self):
        """
        Custom validation for the username field.
        Checks if the username already exists in the database.
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError\
                (self.fields['username'].error_messages['unique'], code='unique')
        return username

    def clean(self):
        """
        Custom validation for the entire form.
        Checks if the two password fields match.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The two password fields didn't match.")
        return cleaned_data

class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating user information. Inherits from Django's UserChangeForm.
    """
    class Meta:
        """
        Metadata for the form.
        Specifies the model and the fields to be included in the form.
        """
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
