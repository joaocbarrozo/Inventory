from django.contrib import admin

from almoxarifado.models import Produto, Fornecedor, Transacao, ProdutoPedido, Pedido

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    pass

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    pass

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    pass

@admin.register(ProdutoPedido)
class ProdutoPedidoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    pass

# Register your models here.
