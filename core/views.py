from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def filter_products(query):
    if query:
        # Construindo a consulta Q para buscar por código ou nome
        filters = Q(name__icontains=query) | Q(code__icontains=query)
        # Aplicando o filtro
        return Product.objects.filter(filters)
    else:
        # Retorna todos os produtos se a query estiver vazia
        return Product.objects.all()

@login_required(login_url='user/login')
def index(request):
    query = request.GET.get('search', '')  # Obtenha a query da barra de pesquisa
    filtered_items = filter_products(query)  # Filtra os produtos baseados na query
    itens_check = Product.objects.filter(is_checked=True)  # Produtos que já foram marcados
    cart = request.session.get('cart', {})  # Obtenha o carrinho da sessão

    if request.method == 'POST':
        if 'items' in request.POST:
            selected_items = request.POST.getlist('items')
            for item_code in selected_items:
                try:
                    product = Product.objects.get(code=item_code)
                    # Definindo o parâmetro desejado como True
                    product.is_checked = True  # Substitua 'some_parameter' pelo nome real do parâmetro
                    product.save()
                except Product.DoesNotExist:
                    continue
            return redirect(reverse('index'))
        elif 'clear_cart' in request.POST:
            # Exemplo de lógica para limpar algo, se necessário
            return redirect(reverse('index'))
        elif 'add_product' in request.POST:
            name = request.POST.get('name')
            price = float(request.POST.get('price'))
            code = request.POST.get('code')
            if name and price and code:
                Product.objects.create(name=name, price=price, code=code)
            return redirect(reverse('index'))

    total = sum(item.price for item in itens_check)

    context = {
        'items': filtered_items,
        'itens_check': itens_check,
        'total': total,
    }
    return render(request, 'core/index.html', context)


@login_required(login_url='user/login')
def clear_cart(request):
    itens = Product.objects.filter(is_checked=True)
    for c in itens:
        c.is_checked = False
        c.save()
    return redirect(reverse('index'))