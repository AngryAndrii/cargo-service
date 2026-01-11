from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(max_length=8)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "license_number", "password1", "password2")