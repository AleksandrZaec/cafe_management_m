from decimal import Decimal
import pytest

from orders.services import calculate_order_total
from orders.models import Order


@pytest.mark.django_db
def test_calculate_order_total(order_with_items: Order) -> None:
    """Тест расчета общей стоимости заказа"""
    order: Order = order_with_items
    expected_total: Decimal = Decimal("300.00")
    total: Decimal = calculate_order_total(order)

    assert total == expected_total
