from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Baby, Record

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
    }))
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
    }))
    
class NewBabyForm(forms.ModelForm):
    class Meta:
        model = Baby
        fields = ['name', 'birth_date', 'birth_weight', 'birth_length']
        widgets = {
                'name': forms.TextInput(),
                'birth_date': forms.DateInput({'type': 'date'}),
                'birth_weight': forms.TextInput(),
                'birth_length': forms.TextInput(),
            }
        
class EditBabyForm(forms.ModelForm):
    class Meta:
        model = Baby
        fields = ['name', 'birth_date', 'birth_weight', 'birth_length']
        widgets = {
                'name': forms.TextInput(),
                'birth_date': forms.DateInput({'type': 'date'}),
                'birth_weight': forms.TextInput(),
                'birth_length': forms.TextInput(),
            }
        
class NewRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['date', 'weight', 'length']
        widgets = {
            'date': forms.DateInput({'type': 'date'}),
            'weight': forms.TextInput(),
            'length': forms.TextInput(),
        }
        
class EditRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['date', 'weight', 'length']
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'weight': forms.TextInput(),
            'length': forms.TextInput(),
        }