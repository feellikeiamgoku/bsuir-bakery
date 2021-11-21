import re
from django import forms
from django.forms.forms import Form
from authenication.models import User

class LoginForm(forms.Form):
    phone = forms.RegexField(r"^\+375([0-9]{1,9})$", widget=forms.TextInput(attrs={
        "placeholder": "Телефон",
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Пароль",
        'class': 'form-control'
    }))

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Пароль",
        'class': 'form-control'
    }))

    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Повторите пароль",
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ["username", "name"]
        widgets = {
            "username": forms.widgets.TextInput(attrs={
                'class': "form-control",
                "placeholder": "Телефон"
            }),
            "name": forms.widgets.TextInput(attrs={
                'class': "form-control",
                "placeholder": "Имя"
            })
        }
        error_messages = {
            "username": {
                "unique": "Пользователь с таким телефонным номером уже существует"
            }
        }


    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password_confirm']

    def clean_username(self):
        cd = self.cleaned_data
        if not re.match(r"^\+375([0-9]{1,9})$", cd["username"]):
            raise forms.ValidationError("Неверно введён телефон")
        return cd["username"]