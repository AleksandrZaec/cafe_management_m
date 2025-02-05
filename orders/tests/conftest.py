import pytest
from decimal import Decimal
from orders.models import Order, OrderItem
from typing import Dict


@pytest.fixture
def order() -> Order:
    """
    Фикстура для создания заказа с блюдами.
    Возвращает объект заказа без элементов.
    """
    return Order.objects.create(table_number=1, total_price=Decimal("150.00"), status="pending")


@pytest.fixture
def order_with_items(order: Order) -> Order:
    """
    Фикстура для создания заказа с блюдами.
    Создает два блюда для переданного заказа.
    """
    OrderItem.objects.create(order=order, name="Пицца", price=Decimal("250.00"))
    OrderItem.objects.create(order=order, name="Лимонад", price=Decimal("50.00"))
    return order


@pytest.fixture
def order1() -> Order:
    """
    Фикстура для создания заказа в статусе "ready".
    """
    return Order.objects.create(table_number=2, total_price=Decimal("200.00"), status="ready")


@pytest.fixture
def order_data() -> Dict[str, str]:
    """
    Фикстура для создания данных нового заказа.
    """
    return {
        'table_number': '1',
        'status': 'pending',
        'orderitem_set-TOTAL_FORMS': '1',
        'orderitem_set-INITIAL_FORMS': '0',
        'orderitem_set-MIN_NUM_FORMS': '0',
        'orderitem_set-MAX_NUM_FORMS': '1000',
        'orderitem_set-0-name': 'Пицца',
        'orderitem_set-0-price': '250.00',
    }
