from django import forms
from django.core.validators import MinLengthValidator

class LoginForm(forms.Form):
    error_css_class = 'alert alert-warning'
    username = forms.CharField(
        max_length=63,
        label='Nom d\'utilisateur',
        validators=[MinLengthValidator(5)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder':'Nom d\'utilisateur'})
    )
    password = forms.CharField(
        max_length=63,
        label='Mot de passe',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'type': 'password'})
    )

class RegisterForm(LoginForm):
    password_confirm = forms.CharField(
        max_length=63,
        label='Conﬁrmer mot de passe',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Conﬁrmer mot de passe',
            'type': 'password'})
    )
