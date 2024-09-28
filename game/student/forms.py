from django import forms
from .models import Role, Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_type']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=12)
    role_id = forms.ModelChoiceField(queryset=Role.objects.all())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'mobile_number', 'role_id', 'date_of_birth')