from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class NewUserForm(UserCreationForm):
    username = forms.EmailField(label='email ')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль ')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторение пароля ')

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class loginForm(forms.Form):
    # username = forms.CharField()
    username = forms.EmailField(label='email ')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class PasswordReset(forms.Form):
    username = forms.EmailField()


class PasswordReset2(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль1')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Пароль2')

    # def clean_password1(self):
    #     password1, password2 = self.cleaned_data["password1"], self.cleaned_data["password2"]
    #     if password1 == password2:
    #         return password1


class makeDiagnoseForm(forms.ModelForm):
    disease = forms.ModelChoiceField(queryset=diagnoses.objects.all(),
                                     to_field_name='name',
                                     label='Выберите диагноз',
                                     empty_label=None, )

    class Meta:
        model = assigned_diagnoses
        fields = ('comment', 'disease',)

