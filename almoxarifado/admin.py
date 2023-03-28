from django.contrib import admin

from almoxarifado.models import Produto, Fornecedor, Transacao

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    pass

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    pass

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    pass

# Register your models here.
