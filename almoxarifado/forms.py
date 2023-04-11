from django import forms
from .models import Produto, Transacao, Pedido, ProdutoPedido

class ProductForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'quantidade', 'estoque_minimo']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['produto', 'usuario', 'fornecedor', 'transacao_tipo', 'quantidade']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = []

class ProdutoPedidoForm(forms.ModelForm):
    class Meta:
        model = ProdutoPedido
        fields = ['produto', 'quantidade']