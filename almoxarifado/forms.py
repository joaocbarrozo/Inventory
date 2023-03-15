from django import forms
from .models import Product, Transaction

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'user', 'company', 'transaction_type', 'quantity']