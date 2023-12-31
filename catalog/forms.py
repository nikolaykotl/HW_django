from django import forms

from catalog.models import Product, Version

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
class ProductForm(StyleFormMixin, forms.ModelForm, ):

    class Meta:
        model = Product
        exclude = ('owner',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_staff = request.user.is_staff
        if is_staff:
            form.base_fields['product_name'].disabled = True
            form.base_fields['purchase_price'].disabled = True
            form.base_fields['owner'].disabled = True
            return form

    def clean_product_name(self):
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        cleaned_data = self.cleaned_data['product_name']

        for item in words:
            if item in cleaned_data.lower():
                raise forms.ValidationError(f'"{item}" запрещено, выберите другое')

        return cleaned_data

    def clean_description_prod(self):
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        cleaned_data = self.cleaned_data['description_prod']

        for word in words:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'"{word}" запрещено, выберите другое')

        return cleaned_data

class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
