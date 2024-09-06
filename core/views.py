from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product, Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Sum



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
    
    # Filtrando por tipo diretamente no banco de dados
    filtered_exames_img = filtered_items.filter(type='IMG')
    filtered_exames_lab = filtered_items.filter(type='LAB')
    filtered_exames_crd = filtered_items.filter(type='CRD')
    
    try:
        cart = Cart.objects.get(user=request.user)  # Tenta obter o carrinho associado ao usuário
    except Cart.DoesNotExist:
        cart = Cart(user=request.user)  # Cria um novo carrinho se não existir
        cart.save()  # Salva o novo carrinho no banco de dados  

    itens_check = cart.product

    if request.method == 'POST':
        if 'items' in request.POST:
            code_items = request.POST.getlist('items')
            selected_items = Product.objects.filter(code__in=code_items)  
            cart.product.add(*selected_items)
            return redirect(reverse('index'))
        elif 'clear_cart' in request.POST:
            # Exemplo de lógica para limpar algo, se necessário
            cart.product.clear()
            cart.save()
            return redirect(reverse('index'))
        elif 'add_product' in request.POST:
            name = request.POST.get('name')
            price = request.POST.get('price')
            code = request.POST.get('code')
            if name and price and code:
                try:
                    price = float(price)
                    Product.objects.create(name=name, price=price, code=code)
                except ValueError:
                    pass  # Trate o erro de conversão de preço, se necessário
            return redirect(reverse('index'))

    total = f"{itens_check.all().aggregate(total_price=Sum('price'))['total_price']or 0:.2f}"

    context = {
        'items': filtered_items,
        'filtered_exames_img': filtered_exames_img,
        'filtered_exames_lab': filtered_exames_lab,
        'filtered_exames_crd': filtered_exames_crd,
        'itens_check': cart.product,
        'total': total,
    }
    return render(request, 'core/index.html', context)
