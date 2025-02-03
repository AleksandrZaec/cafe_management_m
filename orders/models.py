from django.db import models
from decimal import Decimal


class Order(models.Model):
    """Модель заказа в кафе."""

    STATUS_CHOICES: list[tuple[str, str]] = [
        ("pending", "В ожидании"),
        ("ready", "Готово"),
        ("paid", "Оплачено"),
    ]

    id: int
    table_number: int = models.PositiveSmallIntegerField(verbose_name="Номер стола")
    total_price: Decimal = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), verbose_name="Общая стоимость"
    )
    status: str = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус заказа"
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name="Время обновления")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Заказ #{self.id} (Стол {self.table_number}) — {self.get_status_display()}"


class OrderItem(models.Model):
    """Модель блюда в заказе."""

    id: int
    order: Order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ"
    )
    name: str = models.CharField(max_length=255, verbose_name="Название блюда")
    price: Decimal = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена блюда"
    )

    class Meta:
        verbose_name = "Блюдо в заказе"
        verbose_name_plural = "Блюда в заказе"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.name} - {self.price} руб."
