from django import forms
from . models import UserRegister

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model=UserRegister
        fields="__all__"