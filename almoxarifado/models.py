from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    def __str__(self):
        return self.name


class Transaction(models.Model):
    SALE = 'Saida'
    PURCHASE = 'Entrada'
    
    TRANSACTION_TYPES = (
        ('Saida', 'Saida'),
        ('Entrada', 'Entrada'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company.name
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.transaction_type == Transaction.SALE:
            self.product.quantity -= self.quantity
        elif self.transaction_type == Transaction.PURCHASE:
            self.product.quantity += self.quantity
        self.product.save()
       


# Create your models here.
