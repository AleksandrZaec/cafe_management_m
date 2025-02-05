import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    """
    Фильтр заказов по ID и статусу.
    """

    search: django_filters.CharFilter = django_filters.CharFilter(
        field_name="id",
        lookup_expr="iexact",
        label="Order ID"
    )
    status: django_filters.ChoiceFilter = django_filters.ChoiceFilter(
        choices=Order.STATUS_CHOICES,
        label="Статус"
    )

    class Meta:
        model: type[Order] = Order
        fields: list[str] = ["search", "status"]
