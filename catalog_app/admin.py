from django.contrib import admin
from .models import Product, Category

# Register your models here.
# admin.site.register(Student)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category', 'owner',)
    list_filter = ('category', 'owner',)
    search_fields = ('name', 'description', 'owner',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
