from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserInfo

widgets = {
    "username": forms.TextInput(attrs={'class': 'form-control'}),
    "nick_name": forms.TextInput(attrs={'class': 'form-control'}),
    "email": forms.EmailInput(attrs={'class': 'form-control'}),
    "avatar": forms.ClearableFileInput(attrs={'class': 'form-control'}),
    "memo": forms.Textarea(attrs={'class': 'form-control'}),
}


class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserInfo
        fields = ("username", "nick_name", "email", 'avatar', "memo")
        widgets = widgets


class UpdateForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ("username", "nick_name", "email", "avatar", "memo")
        widgets = widgets
