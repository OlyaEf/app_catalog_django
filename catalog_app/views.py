from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog_app.forms import ProductForm, VersionForm
from catalog_app.models import Product, Version


def contacts_view(request):
    return render(request, 'catalog_app/contacts.html')


class ProductListView(ListView):
    model = Product
    template_name = 'catalog_app/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_versions = Version.objects.filter(is_active=True)
        context['active_versions'] = active_versions
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog_app/product_detail.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'catalog_app/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog_app:home')


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'catalog_app/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog_app:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog_app/product_confirm_delete.html'
    success_url = reverse_lazy('catalog_app:home')

