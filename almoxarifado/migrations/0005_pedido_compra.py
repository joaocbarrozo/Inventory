# Generated by Django 4.1.7 on 2023-03-28 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('almoxarifado', '0004_fornecedor_produto_transacao_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveBigIntegerField()),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Aberto', 'aberto'), ('Realizado', 'realizado'), ('Cancelado', 'cancelado')], max_length=20)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almoxarifado.produto')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveBigIntegerField()),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Recebida', 'recebida'), ('Não-Recebida', 'não-recebida'), ('Cancelada', 'cancelada')], max_length=20)),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almoxarifado.fornecedor')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almoxarifado.pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almoxarifado.produto')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]