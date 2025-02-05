from rest_framework import serializers
from orders.models import Order, OrderItem
from orders.services import calculate_order_total
from typing import List, Dict


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор для блюд в заказе."""

    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказа, включая блюда."""

    items: List[OrderItemSerializer]

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'total_price', 'status', 'created_at', 'updated_at', 'items']

    def create(self, validated_data: Dict) -> Order:
        """
        Создает новый заказ с блюдами, рассчитывает общую стоимость и сохраняет его.
        """
        items_data = validated_data.pop('items')

        order = Order.objects.create(**validated_data, status='pending')

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        total_price = calculate_order_total(order)
        order.total_price = total_price
        order.save()

        return order

    def update(self, instance: Order, validated_data: Dict) -> Order:
        items_data = validated_data.pop('items', [])

        instance.table_number = validated_data.get('table_number', instance.table_number)
        instance.status = validated_data.get('status', instance.status)

        if 'total_price' not in validated_data:
            total_price = calculate_order_total(instance)
            instance.total_price = total_price

        instance.save()

        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance
