import pytest
import json
from rest_framework import status
from rest_framework.test import APIClient
from orders.models import Order


@pytest.mark.django_db
def test_create_order(client: APIClient) -> None:
    """Тест создания нового заказа через API."""
    url = '/api/orders/'
    data = {
        'table_number': 2,
        'status': 'pending',
        'items': [
            {'name': 'Паста', 'price': '500.00'},
            {'name': 'Салат', 'price': '150.00'}
        ]
    }

    response = client.post(url, json.dumps(data), content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['table_number'] == 2
    assert len(response.data['items']) == 2
    assert response.data['status'] == 'pending'


@pytest.mark.django_db
def test_update_order_status(client: APIClient, order: Order) -> None:
    """Тест обновления статуса заказа через API."""
    url = f'/api/orders/{order.pk}/'
    data = {
        'status': 'ready',
        'table_number': order.table_number,
        'items': [
            {'name': 'Паста', 'price': '500.00'},
            {'name': 'Салат', 'price': '150.00'}
        ]
    }

    response = client.put(url, data, content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'ready'


@pytest.mark.django_db
def test_delete_order(client: APIClient, order: Order) -> None:
    """Тест удаления заказа через API."""
    url = f'/api/orders/{order.pk}/'
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_orders(client: APIClient, order: Order) -> None:
    """Тест получения списка всех заказов через API."""
    url = '/api/orders/'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_get_order_by_id(client: APIClient, order: Order) -> None:
    """Тест получения конкретного заказа по ID через API."""
    url = f'/api/orders/{order.pk}/'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == order.pk
