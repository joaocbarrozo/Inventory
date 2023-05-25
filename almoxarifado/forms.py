from django import forms
from .models import Produto, Transacao, Pedido, ProdutoPedido

class ProductForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'quantidade', 'estoque_minimo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['produto', 'usuario', 'fornecedor', 'transacao_tipo', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'transacao_tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        def clean_quantidade(self):
            quantidade = self.cleaned_data.get('quantidade')
            produto = self.cleaned_data.get('produto')
            tipo = self.cleaned_data_get('transacao_tipo')

            if quantidade and produto:
                if quantidade > produto.quantidade:
                    raise forms.ValidationError('Quantidade indisponível em estoque.')

            return quantidade

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = []

class ProdutoPedidoForm(forms.ModelForm):
    class Meta:
        model = ProdutoPedido
        fields = ['produto', 'quantidade']