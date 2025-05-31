from django import forms
from .models import Category, Product, Warehouse


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "sku",
            "name",
            "category",
            "cost_price",
            "sell_price",
            "size",
            "color",
        ]
        widgets = {
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control"}),
            "sell_price": forms.NumberInput(attrs={"class": "form-control"}),
            "size": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
        }


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["name", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }
