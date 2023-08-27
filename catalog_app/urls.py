from django.urls import path
from django.views.decorators.cache import cache_page

from catalog_app.views import contacts_view, ProductDetailView, ProductCreateView, ProductListView, ProductUpdateView, \
    ProductDeleteView

app_name = 'catalog_app'

urlpatterns = [
    path('contacts/', contacts_view, name='contacts'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('', ProductListView.as_view(), name='home'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
]
