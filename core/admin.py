from django.contrib import admin
from .models import Product, Cart

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price', 'type')  # Campos a serem exibidos na lista
    search_fields = ('name', 'code')  # Campos a serem pesquisados
    list_filter = ('price',)  # Filtros disponíveis na lateral

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Campos a serem exibidos na lista
    search_fields = ('user',)  # Campos a serem pesquisados
    list_filter = ('user',)  # Filtros disponíveis na lateral

admin.site.register(Product, ProductAdmin)  
admin.site.register(Cart, CartAdmin)  

