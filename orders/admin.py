from typing import Tuple
from django.contrib import admin
from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display: Tuple[str, ...] = ("id", "table_number", "total_price", "status", "created_at")
    list_filter: Tuple[str, ...] = ("status", "created_at")
    search_fields: Tuple[str, ...] = ("table_number",)



