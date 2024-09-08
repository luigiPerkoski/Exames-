from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product, Cart
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse


# Função para filtrar produtos com base no nome ou código
def filter_products(query):
    if query:
        # Construindo a consulta Q para buscar por nome ou código
        filters = Q(name__icontains=query) | Q(code__icontains=query)
        return Product.objects.filter(filters)
    else:
        # Retorna todos os produtos se não houver query
        return Product.objects.all()


# View principal para exibir os produtos e gerenciar o carrinho
def index(request):
    query = request.GET.get('search', '')  # Obter query de busca do formulário
    filtered_items = filter_products(query)  # Filtrar produtos com base na busca

    # Filtrar produtos por tipo (IMG, LAB, CRD)
    filtered_exames_img = filtered_items.filter(type='IMG')
    filtered_exames_lab = filtered_items.filter(type='LAB')
    filtered_exames_crd = filtered_items.filter(type='CRD')

    # Tentar obter o carrinho do usuário ou criar um novo
    cart, created = Cart.objects.get_or_create(user=request.user)

    itens_check = cart.product.all()  # Itens selecionados no carrinho

    # Tratamento de requisições POST (adicionar, limpar carrinho, etc.)
    if request.method == 'POST':
        if 'items' in request.POST:
            code_items = request.POST.getlist('items')  # Obter itens selecionados
            selected_items = Product.objects.filter(code__in=code_items)
            cart.product.add(*selected_items)  # Adicionar produtos ao carrinho
            return redirect(reverse('index'))

        elif 'clear_cart' in request.POST:
            cart.product.clear()  # Limpar o carrinho
            cart.save()
            return redirect(reverse('index'))
        
        elif 'add_product' in request.POST:
            name = request.POST.get('name')
            price = request.POST.get('price')
            code = request.POST.get('code')
            # Validar e criar novo produto
            if name and price and code:
                try:
                    price = float(price)
                    Product.objects.create(name=name, price=price, code=code)
                except ValueError:
                    pass  # Tratar erro de conversão de preço, se necessário
            return redirect(reverse('index'))

        for item in itens_check:
            if f'delete_button_{item.code}' in request.POST:
                cart.product.remove(item)  # Remover produto específico do carrinho
                return redirect(reverse('index'))

    # Cálculo do total dos itens no carrinho
    total = f"{itens_check.aggregate(total_price=Sum('price'))['total_price'] or 0:.2f}"

    context = {
        'items': filtered_items,
        'filtered_exames_img': filtered_exames_img,
        'filtered_exames_lab': filtered_exames_lab,
        'filtered_exames_crd': filtered_exames_crd,
        'itens_check': itens_check,
        'total': total,
    }
    return render(request, 'core/index.html', context)



# Função para gerar o PDF do orçamento
@login_required(login_url='user/login')
def imprimir_orcamento(request):
    cart = Cart.objects.get(user=request.user)  # Obter o carrinho do usuário
    total = f"{cart.product.all().aggregate(total_price=Sum('price'))['total_price'] or 0:.2f}"
    html = render_to_string('core/orcamento_template.html', {'carrinho': cart, 'total': total})

    # Preparar a resposta HTTP para o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="orcamento_{cart.user}.pdf"'

    # Converter HTML para PDF usando xhtml2pdf
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html.encode('utf-8'), dest=pdf)

    # Verificar se houve erro na criação do PDF
    if pisa_status.err:
        return HttpResponse("Erro ao gerar o PDF", status=400)

    # Escrever o PDF na resposta HTTP
    response.write(pdf.getvalue())
    return response
