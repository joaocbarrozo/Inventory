from django.shortcuts import render, redirect
from .models import Produto, Transacao, Pedido, ProdutoPedido
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, TransactionForm, PedidoForm, ProdutoPedidoForm

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
def product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('product')
    else:
        form = ProductForm()
    
    name = request.GET.get('name')
    quantity = request.GET.get('quantity')
    products = Produto.objects.all()
    if name:
        products = products.filter(nome__icontains=name)
    if quantity:
        products = products.filter(quantidade=quantity)
        
    return render(request, 'product.html', {'products': products, 'form': form})

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
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

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
