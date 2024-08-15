from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

@csrf_protect

def index(request):
    return render(request, 'index.html')

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']

        if campo_vazio(nome):
            messages.error(request, 'Nome não pode ficar em branco')
            return redirect('cadastro')
        
        if campo_vazio(email):
            messages.error(request, 'Email não pode ficar em branco')
            return redirect('cadastro')
        
        if senha_diferente(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return redirect('cadastro')
        
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso')
        return redirect('login')
    else:
        return render(request, 'cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Por favor, preencha os campos corretamente')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)

            if verificar_senha(nome, senha) == False:
                messages.error(request, 'Senha Inválida')
                return redirect('login')
            
            else:
                if user is not None:
                    auth.login(request, user)
                    return redirect('index')
        else:
            messages.error(request, 'Usuário Inválido')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def campo_vazio(campo):
    return not campo.strip()

def senha_diferente(senha, senha2):
    return senha != senha2

def verificar_senha(username, password):
    user = User.objects.get(username=username)
    if user.check_password(password):
        return True
    else:
        return False

