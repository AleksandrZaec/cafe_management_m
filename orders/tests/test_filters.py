import pytest
from orders.filters import OrderFilter
from orders.models import Order


@pytest.mark.django_db
def test_filter_by_order_id(order: Order, order1: Order) -> None:
    """Тест фильтрации заказов по ID"""
    filter = OrderFilter({'search': str(order1.id)})
    filtered_orders = filter.qs

    assert filtered_orders.count() == 1
    assert filtered_orders.first() == order1


@pytest.mark.django_db
def test_filter_by_status(order: Order, order1: Order) -> None:
    """Тест фильтрации заказов по статусу"""
    filter = OrderFilter({'status': 'ready'})
    filtered_orders = filter.qs

    assert filtered_orders.count() == 1
    assert filtered_orders.first() == order1


@pytest.mark.django_db
def test_filter_by_id_and_status(order: Order, order1: Order) -> None:
    """Тест комбинированной фильтрации по ID и статусу"""
    filter = OrderFilter({'search': str(order.id), 'status': 'pending'})
    filtered_orders = filter.qs

    assert filtered_orders.count() == 1
    assert filtered_orders.first() == order


@pytest.mark.django_db
def test_filter_no_params(order: Order, order1: Order) -> None:
    """Тест без фильтров (возвращаем все заказы)"""
    filter = OrderFilter({})
    filtered_orders = filter.qs

    assert filtered_orders.count() == 2
