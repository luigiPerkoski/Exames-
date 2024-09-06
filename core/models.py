from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):

    TIPO_PRODUTO_CHOICES = [
        ('LAB', 'Exame de Laboratorio'),
        ('IMG', 'Exame de Imagem'),
        ('CRD', 'Exame Cardiologico'),
    ]

    code = models.CharField(max_length=20, unique=True)  # Código do produto
    name = models.CharField(max_length=300)  # Nome do produto
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço do produto
    type = models.CharField(max_length=3, choices=TIPO_PRODUTO_CHOICES, default='LAB') # Tipo de exame
    is_checked = models.BooleanField(default=False)  # Campo booleano

    def __str__(self):
        return f"{self.code} - {self.name}"

class Cart(models.Model):

    product = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
