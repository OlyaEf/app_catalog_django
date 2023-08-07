from django.urls import path

from catalog_app.views import contacts_view, HomeListView, ProductDetailView

app_name = 'catalog_app'

urlpatterns = [
    path('contacts/', contacts_view, name='contacts'),
    # path('product/<int:pk>/', product_view, name='product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('', HomeListView.as_view(), name='home'),
]
