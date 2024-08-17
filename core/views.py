from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product
from django.db.models import Q


def filter_products(query):
    # Construindo a consulta Q
    filters = Q(name__icontains=query) | Q(code__icontains=query)
    
    # Aplicando o filtro
    return Product.objects.filter(filters)


def index(request):
    query = request.GET.get('search', '')
    filtered_items = filter_products(query)
    itens_check = Product.objects.filter(is_checked=True)
    cart = request.session.get('cart', {})

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



def clear_cart(request):
    itens = Product.objects.all()
    for c in itens:
        c.is_checked = False
        c.save()
    return redirect(reverse('index'))

def criar_novo_objeto(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        novo_campo = request.POST.get('novo_campo')
        
        # Cria um novo objeto na model
        novo_objeto = object.objects.create(
            nome=nome,
            descricao=descricao,
            novo_campo=novo_campo
        )
        
        # Opcional: redireciona para outra página ou exibe uma mensagem
        return redirect('nome_da_sua_view')
