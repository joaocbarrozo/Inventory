from django import forms
from .models import Produto, Transacao

class ProductForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'quantidade', 'estoque_minimo']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['produto', 'usuario', 'fornecedor', 'transacao_tipo', 'quantidade']