from django.shortcuts import get_object_or_404, render, redirect
from .models import Produto, Transacao, Pedido, ProdutoPedido, Entrada, Saida
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProdutoForm, TransactionForm, PedidoForm, ProdutoPedidoForm, EntradasForm, SaidasForm
from django.db.models import Q
from datetime import datetime

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') # replace 'dashboard' with the name of your dashboard view
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
    
@login_required    
def home_view(request):
    products = Produto.objects.all()
    context = {'products': products}
    return render(request, 'home.html', context)

@login_required    
def produtos_view(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produtos')
    else:
        form = ProdutoForm()
    
    #Filtra os produtos por nome, categoria e local
    nome = request.GET.get('nome')
    categoria = request.GET.get('categoria')
    local = request.GET.get('local')
    produtos = Produto.objects.all().order_by("nome")
    if nome:
        produtos = produtos.filter(nome__icontains=nome)
    if categoria:
        produtos = produtos.filter(categoria__categoriaNome__icontains=categoria)
    if local:
        produtos = produtos.filter(local__localNome__icontains=local)        
        
    return render(request, 'produtos.html', {'produtos': produtos, 'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('product')
    else:
        form = ProdutoForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def entradas_view(request):
    entradas = Entrada.objects.all().order_by("-criado_em")

    # Filtra entradas
    produto = request.GET.get('produto')
    tipo = request.GET.get('tipo')
    fornecedor = request.GET.get('fornecedor')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    if data_final:
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    if produto:
        entradas = entradas.filter(Q(produto__nome__icontains=produto))
    if tipo:
        entradas = entradas.filter(Q(tipo__icontains=tipo))
    if fornecedor:
        entradas = entradas.filter(Q(fornecedor__nome__icontains=fornecedor))
    if data_inicial and data_final:
        entradas = entradas.filter(criado_em__range=[data_inicial, data_final])

    return render(request, 'entradas.html', {'entradas': entradas})

@login_required    
def add_entrada_view(request):
    if request.method == 'POST':
        form = EntradasForm(request.POST)
        if form.is_valid():          
            form.save()
            messages.success(request, 'Entrada salva com sucesso!')
            return redirect('entradas')
        else:
            form = EntradasForm()        
            # Redirecione para outra página ou retorne uma resposta de sucesso
            return redirect('product')
    else:
        produto_id = request.GET.get('produto_id')
        user_id = request.GET.get('user_id')
        initial_data = {'produto': produto_id, 'usuario': user_id}
        form = EntradasForm(initial=initial_data)
    return render(request, 'add_entrada.html', {'form': form})  

@login_required    
def saidas_view(request):
    saidas = Saida.objects.all().order_by("-criado_em")
    # Filtra saidas 
    produto = request.GET.get('produto')
    setor = request.GET.get('setor')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    if data_final:
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    if produto:
        saidas = saidas.filter(Q(produto__nome__icontains=produto))
    if setor:
        saidas = saidas.filter(Q(setor__setorNome__icontains=setor))
    if data_inicial and data_final:
        saidas = saidas.filter(criado_em__range=[data_inicial, data_final])
    return render(request, 'saidas.html', {'saidas': saidas})

@login_required
def add_saida_view(request):
    if request.method == 'POST':
        form = SaidasForm(request.POST)
        if form.is_valid():
            quantidade = form.cleaned_data['quantidade']
            produto = form.cleaned_data['produto']
            
            if quantidade > produto.quantidade:
                # The entered quantity exceeds the available stock
                # Display an appropriate error message to the user
                form.add_error('quantidade', 'A quantidade informada excede o estoque disponível.')
            else:
                form.save()
                messages.success(request, 'Saída salva com sucesso!')
                return redirect('saidas')
        # If the form is invalid, render the form with errors
    else:
        produto_id = request.GET.get('produto_id')
        user_id = request.GET.get('user_id')
        initial_data = {'produto': produto_id, 'usuario': user_id}
        form = SaidasForm(initial=initial_data)
    
    return render(request, 'add_saida.html', {'form': form})

@login_required    
def pedidos_view(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido salvo com sucesso!')
            return redirect('pedidos')
    else:
        form = PedidoForm()
    
    pedidos = Pedido.objects.all().order_by("-criado_em")
    #Filtra os produtos por nome, categoria e local
    id = request.GET.get('id')
    fornecedor = request.GET.get('fornecedor')
    status = request.GET.get('status')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    if data_final:
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
    
    if id:
        pedidos = pedidos.filter(id__icontains=id)
    if fornecedor:
        pedidos = pedidos.filter(fornecedor__nome__icontains=fornecedor)
    if status:
        pedidos = pedidos.filter(status__icontains=status)        
        
    return render(request, 'pedidos.html', {'pedidos': pedidos, 'form': form})

@login_required
def add_produto_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        form = ProdutoPedidoForm(request.POST)
        if form.is_valid():
            produto_pedido = form.save(commit=False)
            produto_pedido.pedido = pedido
            produto_pedido.save()
            messages.success(request, 'Produto adicionado ao pedido com sucesso!')
            return redirect('detalhes_pedido', pedido_id=pedido.id)
    else:
        form = ProdutoPedidoForm()

    todos_produtos = Produto.objects.all()  # Obtenha todos os produtos disponíveis

    return render(request, 'detalhes_pedido.html', {'form': form, 'pedido': pedido, 'todos_produtos': todos_produtos})


@login_required
def detalhes_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    produtos = pedido.produtos.all()
    
    return render(request, 'detalhes_pedido.html', {'pedido': pedido, 'produtos': produtos})


@login_required    
def transaction_log(request):
    transactions = Transacao.objects.all()
     # Filter transactions by product name
    product_name = request.GET.get('product_name')
    if product_name:
        transactions = transactions.filter(produto__nome__icontains=product_name)

    # Filter transactions by transaction type
    transaction_type = request.GET.get('transaction_type')
    if transaction_type:
        transactions = transactions.filter(transacao_tipo=transaction_type)
    return render(request, 'transaction_log.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            quantidade = form.cleaned_data['quantidade']
            produto = form.cleaned_data['produto']
            tipo = form.cleaned_data['transacao_tipo']

            if tipo == 'Saida' and quantidade > produto.quantidade:
                # A quantidade informada excede a quantidade disponível em estoque
                # Exiba uma mensagem de erro adequada para o usuário
                form.add_error('quantidade', 'A quantidade informada excede o estoque disponível.')
            else:
                # A quantidade informada está disponível em estoque ou é uma transação de entrada
                # Faça o processamento adicional e salve o objeto Transacao
                transacao = form.save()
                
                if tipo == 'saida':
                    # Restrinja a quantidade no estoque apenas para transações de saída
                    produto.quantidade -= quantidade
                    produto.save()

                # Redirecione para outra página ou retorne uma resposta de sucesso
                return redirect('product')
    else:
        product_id = request.GET.get('product_id')
        user_id = request.GET.get('user_id')
        initial_data = {'produto': product_id, 'usuario': user_id}
        form = TransactionForm(initial=initial_data)
    return render(request, 'add_transaction.html', {'form': form})
    
@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(status='Realizado')
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

@login_required
def criar_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        produto_pedido_form = ProdutoPedidoForm(request.POST)
        if pedido_form.is_valid() and produto_pedido_form.is_valid():
            pedido = pedido_form.save(commit=False)
            pedido.status = 'Aberto'
            pedido.solicitante = request.user
            pedido.save()
            produto_pedido = produto_pedido_form.save(commit=False)
            produto_pedido.pedido = pedido
            produto_pedido.save()
            return redirect('lista_pedido')
    else:
        pedido_form = PedidoForm()
        produto_pedido_form = ProdutoPedidoForm()
    return render(request, 'criar_pedido.html', {'pedido_form': pedido_form, 'produto_pedido_form': produto_pedido_form})


# Create your views here.
