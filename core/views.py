from django.shortcuts import render, redirect
from django.urls import reverse

# Lista de itens e valores
ITENS = [
    {"nome": "maca", "preco": 1.00, "codigo": "MA"},
    {"nome": "banana", "preco": 2.00, "codigo": "BA"},
    {"nome": "laranja", "preco": 1.50, "codigo": "LA"},
]

def index(request):
    query = request.GET.get('search', '')
    filtered_items = [item for item in ITENS if query.lower() in item['nome'].lower()]
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        if 'items' in request.POST:
            selected_items = request.POST.getlist('items')
            for item_code in selected_items:
                for item in ITENS:
                    if item['codigo'] == item_code:
                        item_name = item['nome']
                        if item_name in cart:
                            cart[item_name] += 1
                        else:
                            cart[item_name] = 1
            request.session['cart'] = cart
            return redirect(reverse('index'))
        elif 'clear_cart' in request.POST:
            request.session['cart'] = {}
            return redirect(reverse('index'))
        elif 'add_product' in request.POST:
            # Adiciona novo produto à lista ITENS
            name = request.POST.get('name')
            price = float(request.POST.get('price'))
            code = request.POST.get('code')
            if name and price and code:
                ITENS.append({"nome": name, "preco": price, "codigo": code})
            return redirect(reverse('index'))

    # Calculando o subtotal e total
    item_subtotals = {}
    for item_name, quantity in cart.items():
        item = next((i for i in ITENS if i['nome'] == item_name), None)
        if item:
            item_subtotals[item_name] = item['preco'] * quantity

    total = sum(item_subtotals.values())
    
    context = {
        'items': filtered_items,
        'cart': cart,
        'total': total,
        'item_prices': {item['nome']: item['preco'] for item in ITENS},
        'item_subtotals': item_subtotals
    }
    return render(request, 'core/index.html', context)


def clear_cart(request):
    request.session['cart'] = {}
    return redirect(reverse('index'))
