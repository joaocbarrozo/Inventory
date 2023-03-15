from django.contrib import admin

from almoxarifado.models import Product, Company, Transaction


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass

# Register your models here.
