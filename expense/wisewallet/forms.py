# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Assuming your models are in the same directory or update the import path

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser  # Use your custom user model here
        fields = ['username', 'email', 'password1', 'password2']
# forms.py

from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['user','date', 'label', 'value']
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=user.pk)