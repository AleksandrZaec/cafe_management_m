from decimal import Decimal
import pytest

from orders.models import Order, OrderItem


@pytest.mark.django_db
def test_order_creation() -> None:
    """Тест создания заказа"""
    order: Order = Order.objects.create(table_number=1, total_price=Decimal("150.00"), status="pending")
    assert order.id is not None
    assert order.table_number == 1
    assert order.total_price == Decimal("150.00")
    assert order.status == "pending"


@pytest.mark.django_db
def test_order_str(order: Order) -> None:
    """Тест строкового представления заказа"""
    assert str(order) == f"Заказ #{order.id} (Стол {order.table_number}) — В ожидании"


@pytest.mark.django_db
def test_order_status_display(order: Order) -> None:
    """Тест отображения статуса заказа"""
    assert order.get_status_display() == "В ожидании"


@pytest.mark.django_db
def test_order_item_creation(order: Order) -> None:
    """Тест создания блюда в заказе"""
    item: OrderItem = OrderItem.objects.create(order=order, name="Пицца", price=Decimal("250.00"))
    assert item.id is not None
    assert item.order == order
    assert item.name == "Пицца"
    assert item.price == Decimal("250.00")


@pytest.mark.django_db
def test_order_item_str(order_with_items: Order) -> None:
    """Тест строкового представления блюда"""
    item: OrderItem = order_with_items.items.first()
    assert str(item) == f"{item.name} - {item.price} руб."
