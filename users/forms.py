from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from distribution.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar',)


    password = forms.CharField(widget=forms.HiddenInput(), required=False)
