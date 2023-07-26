from django.urls import path

from catalog_app.views import product_view, contacts_view, home_view

app_name = 'catalog_app'

urlpatterns = [
    path('contacts/', contacts_view, name='contacts'),
    path('product/<int:pk>/', product_view, name='product'),
    path('', home_view, name='home'),
]
