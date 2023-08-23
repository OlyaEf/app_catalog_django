from django import forms

from catalog_app.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'description', 'is_published', 'owner')

    def __check(self, field):
        banned_words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар')
        cleaned_data = self.cleaned_data[field]
        for word in banned_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Использовано запрещенное слово: <<{word}>>.')
        return cleaned_data

    def clean_name(self):
        return self.__check('name')

    def clean_description(self):
        return self.__check('description')


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('product', 'version_name', 'version_number')

    # Добавьте поле выбора активной версии
    active_version = forms.BooleanField(required=False, label="Активная версия")
