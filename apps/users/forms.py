from django import forms
from .models import User, Role


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Parol"
    )

    class Meta:
        model = User
        fields = ["username", "email", "role", "phone", "password", "avatar"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-select"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        raw = self.cleaned_data["password"]
        if raw:
            user.set_password(raw)
        if commit:
            user.save()
        return user
