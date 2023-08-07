from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView

from catalog_app.models import Product, Category


# Create your views here.
def contacts_view(request):
    return render(request, 'catalog_app/contacts.html')


class HomeListView(ListView):
    model = Product
    template_name = 'catalog_app/home.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog_app/product_detail.html'
