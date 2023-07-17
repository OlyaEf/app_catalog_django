from django.urls import path

from catalog_app.views import contacts_view, home_view

urlpatterns = [
    path('contacts/', contacts_view),
    path('', home_view)
]
