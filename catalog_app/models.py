from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(**NULLABLE, verbose_name='описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Продукт')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='product_image/', verbose_name='превью', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.category})'

    def save(self, *args, **kwargs):
        if self.image:
            # Получаем имя файла изображения
            filename = self.image.name
            # Генерируем уникальное имя файла, чтобы избежать перезаписи файлов с одинаковыми именами
            unique_filename = f"product_photos/{slugify(self.name)}_{filename}"
            # Устанавливаем уникальное имя файла в поле image
            self.image.name = unique_filename

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_photos/', verbose_name='фотография продукта')

    def __str__(self):
        return f'Фотография продукта: {self.product.name}'
