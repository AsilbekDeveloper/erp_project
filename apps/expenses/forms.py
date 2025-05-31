from django import forms
from .models import ExpenseCategory, Expense
from apps.inventory.models import Category, Product


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["category", "product", "amount", "note"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "product": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }
