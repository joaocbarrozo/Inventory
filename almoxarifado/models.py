from django.db import models
from django.contrib.auth.models import User

class Setor(models.Model):
    setorNome = models.CharField(max_length=64)
    def __str__(self):
        return self.setorNome
    
class Categoria(models.Model):
    categoriaNome = models.CharField(max_length=64)
    def __str__(self):
        return self.categoriaNome

class LocalPrateleira(models.Model):
    localNome = models.CharField(max_length=64)
    def __str__(self):
        return self.localNome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    quantidade = models.PositiveIntegerField()
    estoque_minimo = models.PositiveIntegerField()
    #categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    #setor = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    #local = models.ForeignKey(LocalPrateleira, on_delete=models.CASCADE)
    #preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    #validade = models.DateField()
    
    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    fone = models.CharField(max_length=20)
    email = models.EmailField()
    def __str__(self):
        return self.nome


class Transacao(models.Model):
    SAIDA = 'Saida'
    ENTRADA = 'Entrada'
    
    TRANSACTION_TYPES = (
        ('Saida', 'Saida'),
        ('Entrada', 'Entrada'),
    )

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    transacao_tipo = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantidade = models.PositiveIntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fornecedor.nome
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.transacao_tipo == Transacao.SAIDA:
            self.produto.quantidade -= self.quantidade
        elif self.transacao_tipo == Transacao.ENTRADA:
            self.produto.quantidade += self.quantidade
        self.produto.save()
       
class Pedido(models.Model):
    STATUS = (
        ('Aberto', 'aberto'),
        ('Realizado', 'realizado'),
        ('Cancelado', 'cancelado')
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)

class ProdutoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveBigIntegerField()


class Compra(models.Model):
    STATUS = (
        ('Recebida', 'recebida'),
        ('Não-Recebida', 'não-recebida'),
        ('Cancelada', 'cancelada')
    )    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveBigIntegerField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE) 




# Create your models here.
