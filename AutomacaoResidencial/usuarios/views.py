from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = authenticate(
            request,
            username=email,
            password=senha
        )

        if usuario is not None:

            login(request, usuario)

            return redirect('dashboard')

        else:

            messages.error(
                request,
                'E-mail ou senha incorretos.'
            )

            return redirect('login')

    return render(request, 'usuarios/login.html')


def cadastro(request):

    if request.method == 'POST':

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Verifica se as senhas são iguais
        if senha != confirmar_senha:

            messages.error(
                request,
                'As senhas não coincidem.'
            )

            return redirect('cadastro')


        # Verifica se o e-mail já existe
        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                'Este e-mail já está cadastrado.'
            )

            return redirect('cadastro')


        # Cria o usuário
        usuario = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome
        )

        usuario.save()


        messages.success(
            request,
            'Cadastro realizado com sucesso!'
        )

        return redirect('login')


    return render(request, 'usuarios/cadastro.html')

@never_cache
@login_required
def dashboard(request):

    return render(request, 'usuarios/dashboard.html')


def logout_view(request):

    logout(request)

    return redirect('login')