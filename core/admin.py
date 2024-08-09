from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price')  # Campos a serem exibidos na lista
    search_fields = ('name', 'code')  # Campos a serem pesquisados
    list_filter = ('price',)  # Filtros disponíveis na lateral

admin.site.register(Product, ProductAdmin)  

