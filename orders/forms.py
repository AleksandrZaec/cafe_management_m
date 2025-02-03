from typing import Type
from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model: Type[Order] = Order
        fields: list[str] = ["table_number", "status"]