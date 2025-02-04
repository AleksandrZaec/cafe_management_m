from typing import Type
from django import forms
from orders.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    """ Форма для создания и обновления заказа."""
    class Meta:
        model: Type[Order] = Order
        fields: list[str] = ["table_number", "status"]


class OrderItemForm(forms.ModelForm):
    """ Форма для создания и обновления позиции в заказе."""
    class Meta:
        model: Type[Order] = OrderItem
        fields: list[str] = ["name", "price"]
