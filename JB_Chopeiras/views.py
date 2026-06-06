from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')


def sair(request):
    logout(request)
    return redirect('home')


def tela_entrada(request):
    mensagem = None

    if request.method == 'POST':
        tipo_form = request.POST.get('tipo_form')

        if tipo_form == 'login':
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('senha', '').strip()

            if not email or not senha:
                mensagem = 'Preencha email e senha.'
            else:
                try:
                    usuario_obj = User.objects.get(email=email)
                    usuario = authenticate(request, username=usuario_obj.username, password=senha)
                    if usuario is not None:
                        login(request, usuario)
                        return redirect('servicosPage' if usuario.is_staff else 'home')
                    else:
                        mensagem = 'Usuário ou senha inválida.'
                except User.DoesNotExist:
                    mensagem = 'Usuário ou senha inválida.'

        elif tipo_form == 'registro':
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('senha', '').strip()
            confirmar_senha = request.POST.get('confirmar_senha', '').strip()

            if not email or not senha or not confirmar_senha:
                mensagem = 'Preencha todos os campos obrigatórios.'
            elif senha != confirmar_senha:
                mensagem = 'As senhas não coincidem.'
            elif User.objects.filter(username=email).exists():
                mensagem = 'Já existe um usuário com esse email.'
            else:
                usuario = User.objects.create_user(
                    username=email,
                    email=email,
                    password=senha
                )
                login(request, usuario)
                return redirect('home')

    return render(request, 'login.html', {'mensagem': mensagem})