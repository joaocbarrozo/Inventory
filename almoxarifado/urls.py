"""Inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import login_view, home_view, product_view, logout_view, transaction_log, add_product, add_transaction, lista_pedidos, criar_pedido

urlpatterns = [
    # other URL patterns
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('product/', product_view, name='product'),
    path('transaction/', transaction_log, name='transaction_log'),
    path('add-product/', add_product, name='add_product'),
    path('add-transaction/', add_transaction, name='add_transaction'),
    path('lista-pedidos/', lista_pedidos, name='pedidos'),
    path('criar-pedidos/', criar_pedido, name='criar_pedido'),
]

