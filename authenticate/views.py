from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import forms

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('review:accueil-review')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'authenticate/accueil.html',
        context={'form': form, 'message': message}
    )

def register_page(request):
    form = forms.RegisterForm()
    message = ''

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            print(vars(form))
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['password_confirm']
            username = form.cleaned_data['username']
            if password1 != password2:
                form.add_error('password', 'Les deux champs mot de passe ne correpondent pas')
            else:
                user = User.objects.create_user(username, '', password1)
                user.save()
                user = authenticate(request, username=user, password=password1)
                login(request, user)
                return redirect('review:accueil-review')

    return render(request, 'authenticate/register.html', {'form': form})

def logout_page(request):
	logout(request)
	return redirect(reverse('authenticate:login'))
