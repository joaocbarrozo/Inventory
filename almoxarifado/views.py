from django.shortcuts import render, redirect
from .models import Produto, Transacao
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, TransactionForm

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
    name = request.GET.get('name')
    quantity = request.GET.get('quantity')
    products = Produto.objects.all()
    if name:
        products = products.filter(nome__icontains=name)
    if quantity:
        products = products.filter(quantidade=quantity)
    return render(request, 'product.html', {'products': products})

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
            form.save()
            return redirect('product')
    else:
        product_id = request.GET.get('product_id')
        user_id = request.GET.get('user_id')
        initial_data = {'produto': product_id, 'usuario': user_id}
        form = TransactionForm(initial=initial_data)
    return render(request, 'add_transaction.html', {'form': form})
    

# Create your views here.
