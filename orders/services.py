from decimal import Decimal
from django.db.models import Sum
from django.utils.timezone import localdate
from orders.models import Order
from typing import Optional


def calculate_order_total(order: Order) -> Decimal:
    """Вычисляет общую стоимость заказа на основе связанных блюд."""
    total: Optional[Decimal] = order.items.aggregate(total=Sum("price"))["total"]
    return total or Decimal("0.00")


def get_daily_revenue() -> Decimal:
    """Подсчитывает общую выручку за сегодняшний день (оплаченные заказы)."""
    today = localdate()
    total: Optional[Decimal] = Order.objects.filter(
        created_at__date=today, status="paid"
    ).aggregate(total=Sum("total_price"))["total"]
    return total or Decimal("0.00")
