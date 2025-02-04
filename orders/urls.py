from django.urls import path

from orders import views
from orders.apps import OrdersConfig
from orders.views import (
    OrderListView, OrderCreateView, OrderUpdateView,
    OrderDetailView, OrderDeleteView)

app_name = OrdersConfig.name

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("order/<int:pk>/edit/", OrderUpdateView.as_view(), name="order_update"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("order/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path('revenue/', views.revenue_view, name='revenue'),

]
