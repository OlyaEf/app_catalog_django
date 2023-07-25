from django.core.management import BaseCommand

from catalog_app.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        category_list = [
            {'name': 'Category 1', 'description': 'Description of Category 1'},
            {'name': 'Category 2', 'description': 'Description of Category 2'},
            {'name': 'Category 3', 'description': 'Description of Category 3'},
        ]
        product_list = [
            {'name': 'Product 1', 'description': 'Description of Product 1', 'price': 10.99, 'category': 'Category 1'},
            {'name': 'Product 2', 'description': 'Description of Product 2', 'price': 19.99, 'category': 'Category 2'},
            {'name': 'Product 3', 'description': 'Description of Product 3', 'price': 26.99, 'category': 'Category 3'},
        ]
        self.clear_data()
        self.create_data(category_list, product_list)
        self.stdout.write(self.style.SUCCESS('Database has been successfully filled!'))

    def clear_data(self):
        self.stdout.write('Clearing old data')
        Category.objects.all().delete()
        Product.objects.all().delete()

    def create_data(self, category_list, product_list):
        self.stdout.write('Creating new data')
        for category_data in category_list:
            Category.objects.create(**category_data)

        for product_data in product_list:
            category_name = product_data.pop('category')
            category = Category.objects.get(name=category_name)
            Product.objects.create(category=category, **product_data)

