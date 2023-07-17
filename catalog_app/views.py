from django.shortcuts import render


# Create your views here.
def contacts_view(request):
    return render(request, 'catalog_app/contacts.html')


def home_view(request):
    return render(request, 'catalog_app/home.html')
