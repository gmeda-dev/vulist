from django import forms
from accounts.models import User

from home.models import Product, Vulnerability

class FilterQueryForm(forms.Form):
    search = forms.CharField(required=False)
    product_field_filter = forms.ModelChoiceField(required=False, queryset=Product.objects.none())

    def __init__(self):
        super().__init__()

        choices = [('', 'Select Product')]
        for product in Product.objects.all().order_by('name'):
            choices.append((product.name, product.name))

        self.fields['search'].widget.attrs['placeholder'] = 'Search by ID or title'

        self.fields['product_field_filter'].choices = tuple(choices)
        self.fields['product_field_filter'].widget.attrs['style'] = 'width: 300px'


class MarkVulnerabilityForm(forms.Form):
    value = forms.BooleanField(required=False)
    id = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        try:
            vulnerability = Vulnerability.objects.get(id=self.data['id'])
            cleaned_data['vulnerability'] = vulnerability
        except Vulnerability.DoesNotExist:
            raise forms.ValidationError('Does not exist')

        return cleaned_data


class EditVulnerabilityForm(forms.ModelForm):
    class Meta:
        model = Vulnerability
        exclude = (
            'id',
        )