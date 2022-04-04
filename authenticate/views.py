from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import forms


def login_page(request):
    html_template = 'authenticate/accueil.html'
    form = forms.LoginForm()
    context = {}
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
                context['message'] = 'Identifiants invalides.'
    context['form'] = form
    return render(request, html_template, context=context)


def register_page(request):
    form = forms.RegisterForm()

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            print(vars(form))
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['password_confirm']
            username = form.cleaned_data['username']
            if password1 != password2:
                form.add_error(
                    'password',
                    'Les deux champs mot de passe ne correpondent pas'
                )
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
