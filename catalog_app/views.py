from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog_app.forms import ProductForm, VersionForm
from catalog_app.models import Product, Version
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied


def contacts_view(request):
    return render(request, 'catalog_app/contacts.html')


class ProductListView(ListView):
    model = Product
    template_name = 'catalog_app/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        active_versions = Version.objects.filter(is_active=True)
        context['active_versions'] = active_versions
        return context


@method_decorator(login_required(login_url='users:register'), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog_app/product_detail.html'


@method_decorator(login_required(login_url='users:register'), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    template_name = 'catalog_app/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog_app:home')

    def form_validate(self, form):
        response = super().form_valid(form)
        self.object.owner = self.request.user
        self.object.save()
        return response


@method_decorator(login_required(login_url='users:register'), name='dispatch')
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

        active_version_id = self.request.POST.get('active_version')  # Получаем значение из POST
        if active_version_id:
            active_version = Version.objects.get(id=active_version_id)
            active_version.is_active = True
            active_version.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверка, что текущий пользователь - владелец продукта
        if self.object.owner != request.user and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required(login_url='users:register'), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog_app/product_confirm_delete.html'
    success_url = reverse_lazy('catalog_app:home')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверка, что текущий пользователь - владелец продукта
        if self.object.owner != request.user and not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
