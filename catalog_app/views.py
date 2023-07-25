from django.shortcuts import render

from catalog_app.models import Product


# Create your views here.
def contacts_view(request):
    return render(request, 'catalog_app/contacts.html')


def home_view(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Каталог - Наши услуги'
    }
    return render(request, 'catalog_app/home.html', context)
