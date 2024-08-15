from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from produtos.models import Produto, ItemCarrinho
from django.http import JsonResponse
import inflect

from django.views.decorators.csrf import csrf_protect

@csrf_protect

def catalogo(request):
    filtra_categoria = request.GET.get('categoria')
    print(f"Categoria do Filtro: {filtra_categoria}")
    
    produtos = Produto.objects.all()

    if filtra_categoria and filtra_categoria.lower() != 'todos':
        p = inflect.engine()
        categoria_singular = p.singular_noun(filtra_categoria) or filtra_categoria
        produtos = produtos.filter(categoria__iexact=categoria_singular)

    contexto = {'produtos': produtos}
    return render(request, 'catalogo.html', contexto)

def cad_produtos(request):
    return render(request, 'cad-produtos.html')

def cadastrar(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        categoria = request.POST['categoria']
        img1 = request.FILES['imagem1']
        img2 = request.FILES['imagem2']
        preco = request.POST['preco']

        produto = Produto.objects.create(nome_produto=nome, categoria=categoria, imagem1=img1, imagem2=img2, preco=preco)
        produto.save()
        messages.success(request, 'Produto cadastrado com sucesso')
        return redirect('cad_produtos')
    
    else:
        messages.error(request, 'Produto não cadastrado, tente novamente')
        return render(request, 'cad_produto')

def carrinho(request):
    if request.user.is_authenticated:
        itens_carrinho = ItemCarrinho.objects.all()
        total_carrinho = sum(item.preco_total for item in itens_carrinho)

        contexto = {'itens_carrinho': itens_carrinho, 'total_carrinho': total_carrinho}
        return render(request, 'carrinho.html', contexto)
    else:
        messages.error(request, 'Usuário precisa estar logado')
        return redirect('login')

def aumenta_item(request, item_id):
    item = get_object_or_404(ItemCarrinho, pk=item_id)
    item.quantidade += 1
    item.save()
    return redirect('carrinho')

def diminui_item(request, item_id):
    item = get_object_or_404(ItemCarrinho, pk=item_id)
    if item.quantidade > 1:
        item.quantidade -= 1
        item.save()
    else:
        item.delete()
    return redirect('carrinho')

def excluir_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, pk=item_id)
    item.delete()
    return redirect('carrinho')

def adicionar_ao_carrinho(request, produto_id):
    if request.user.is_authenticated:
        produto = Produto.objects.get(pk=produto_id)
        quantidade = int(request.POST.get('quantidade', 1))

        if ItemCarrinho.objects.filter(produto=produto).exists():
            item_carrinho = ItemCarrinho.objects.get(produto=produto)
            item_carrinho.quantidade += quantidade
            item_carrinho.preco_total = item_carrinho.quantidade * item_carrinho.preco_unitario
            item_carrinho.save()
        else:
            preco_unitario = produto.preco
            preco_total = quantidade * preco_unitario
            ItemCarrinho.objects.create(produto=produto, quantidade=quantidade, preco_unitario=preco_unitario, preco_total=preco_total)
        
        return redirect('catalogo')
    else:
        messages.error(request, 'Usuário precisa estar logado')
        return redirect('login')

def get_cart_count(request):
    carrinho = request.session.get('carrinho', [])
    cart_count = len(carrinho)
    return JsonResponse({'cart_count': cart_count})
