from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    quantidade = models.PositiveIntegerField()
    estoque_minimo = models.PositiveIntegerField()
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
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveBigIntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)

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
