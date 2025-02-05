from django.urls import path, include
from orders import views
from orders.api_views import OrderViewSet, DailyRevenueView
from orders.apps import OrdersConfig
from orders.views import (
    OrderListView, OrderCreateView, OrderUpdateView,
    OrderDetailView, OrderDeleteView)
from rest_framework.routers import DefaultRouter

app_name = OrdersConfig.name
router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("order/<int:pk>/edit/", OrderUpdateView.as_view(), name="order_update"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("order/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path('revenue/', views.revenue_view, name='revenue'),

    path('api/', include(router.urls)),
    path('api/revenue/', DailyRevenueView.as_view(), name='daily_revenue'),

]
