import pytest
from django.urls import reverse
from django.test import Client
from orders.models import Order
from typing import Any


@pytest.mark.django_db
def test_order_create_view_invalid_data(client: Client) -> None:
    """Тест создания заказа с неверными данными"""
    url = reverse('orders:order_create')
    invalid_data = {
        'table_number': '',
        'status': 'pending',
        'orderitem_set-TOTAL_FORMS': 1,
        'orderitem_set-INITIAL_FORMS': 0,
        'orderitem_set-MIN_NUM_FORMS': 0,
        'orderitem_set-MAX_NUM_FORMS': 1000,
        'orderitem_set-0-name': 'Пицца',
        'orderitem_set-0-price': '250.00',
    }
    response: Any = client.post(url, invalid_data)

    assert response.status_code == 200
    assert 'This field is required.' in response.content.decode()


@pytest.mark.django_db
def test_order_delete_view(client: Client, order: Order) -> None:
    """Тест удаления заказа"""
    url = reverse('orders:order_delete', args=[order.pk])
    response: Any = client.post(url)

    assert response.status_code == 302
    assert not Order.objects.filter(pk=order.pk).exists()


@pytest.mark.django_db
def test_create_order(api_client):
    """Тест создания заказа"""
    payload = {
        "table_number": 2,
        "items": [
            {"name": "Burger", "price": "10.50"},
            {"name": "Fries", "price": "5.00"}
        ]
    }
    response = api_client.post("/api/orders/", payload, format='json')
    assert response.status_code == 201
    assert response.data["table_number"] == 2
    assert "id" in response.data


@pytest.mark.django_db
def test_update_order(api_client, create_order):
    """Тест обновления статуса заказа"""
    payload = {"table_number": 10, "status": "completed"}
    response = api_client.patch(f"/api/orders/{create_order.id}/", payload, format='json')
    assert response.status_code == 200
    assert response.data["table_number"] == 10
    assert response.data["status"] == "completed"
