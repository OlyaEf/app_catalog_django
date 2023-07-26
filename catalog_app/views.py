from django.shortcuts import render, get_object_or_404

from catalog_app.models import Product, Category


# Create your views here.
def contacts_view(request):
    return render(request, 'catalog_app/contacts.html')


def home_view(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Каталог - Наши услуги'
    }
    return render(request, 'catalog_app/home.html', context)


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'title': f'Наши услуги {product.name}'
    }
    return render(request, 'catalog_app/product_detail.html', context)

