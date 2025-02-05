from typing import Type
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.services import get_daily_revenue


class OrderViewSet(viewsets.ModelViewSet):
    """
    Предоставляет операции CRUD для создания, получения, обновления и удаления заказов.
    """
    queryset: Type[Order] = Order.objects.all()
    serializer_class: Type[OrderSerializer] = OrderSerializer


class DailyRevenueView(APIView):
    """
    Возвращает сумму всех оплаченных заказов, созданных сегодня.
    """

    def get(self, request, *args, **kwargs):
        try:
            revenue = get_daily_revenue()
            return Response({"daily_revenue": str(revenue)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
