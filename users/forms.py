from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from users.models import Profile


class DateInput(forms.DateInput):
    # Custom field for birth date
    input_type = "date"


class UserRegisterForm(UserCreationForm):
    """
    User registration form
    """
    first_name = forms.CharField(max_length=100, label=_("First name"))
    last_name = forms.CharField(max_length=100, label=_("Last name"))
    email = forms.EmailField(max_length=150, widget=forms.EmailInput, label=_("Email"))
    birth_date = forms.DateTimeField(widget=DateInput(), required=False, label=_("Birth date"))

    class Meta:
        """
        Configure form
        """

        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class UserLoginForm(forms.Form):
    """
    User login form
    """
    email = forms.EmailField(max_length=150, widget=forms.EmailInput, label=_("Email"))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, label=_("Password"))

    class Meta:
        model = User
        fields = ["email", "password"]


class UserUpdateForm(forms.ModelForm):
    """
    Update user form
    """
    email = forms.EmailField(max_length=150, widget=forms.EmailInput, label=_("Email"))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    """
    User profile form
    """
    birth_date = forms.DateTimeField(widget=DateInput(), required=False, label=_("Birth date"))

    class Meta:
        model = Profile
        fields = ["birth_date", "image"]
