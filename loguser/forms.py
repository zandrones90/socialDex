from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ip
from django import forms
#il model della sezione admin


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2'
                  ]


class IpForm(forms.ModelForm):
    class Meta:
        model = Ip
        fields = ['user', 'ip']



