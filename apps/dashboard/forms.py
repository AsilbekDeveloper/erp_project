from django import forms
from datetime import date
from datetime import datetime

YEAR_CHOICES = [(y, y) for y in range(2022, date.today().year + 1)]


class StatsFilterForm(forms.Form):
    year = forms.ChoiceField(
        choices=[
            (y, y) for y in range(datetime.today().year, datetime.today().year - 6, -1)
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
