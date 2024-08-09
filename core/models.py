from django.db import models

class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)  # Código do produto
    name = models.CharField(max_length=300)  # Nome do produto
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço do produto
    is_checked = models.BooleanField(default=False)  # Campo booleano

    def __str__(self):
        return f"{self.code} - {self.name}"
