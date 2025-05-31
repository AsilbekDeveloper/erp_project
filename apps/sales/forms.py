from django import forms
from django.forms import inlineformset_factory

from .models import Customer, SaleOrder, SaleOrderLine


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "phone", "address")
        widgets = {f: forms.TextInput(attrs={"class": "form-control"}) for f in fields}


class SaleOrderForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = ("customer", "note")
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }


class SaleOrderLineForm(forms.ModelForm):
    class Meta:
        model = SaleOrderLine
        fields = ("product", "quantity", "price")
        widgets = {
            "product": forms.Select(attrs={"class": "form-select product-select"}),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control qty-input", "min": 1}
            ),
        }


SaleLineFormSet = inlineformset_factory(
    SaleOrder,
    SaleOrderLine,
    form=SaleOrderLineForm,
    extra=1,
    can_delete=True,
)
