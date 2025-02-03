from typing import Any, Dict
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from orders.models import Order
from orders.forms import OrderForm


class OrderListView(FilterView):
    model = Order
    template_name: str = "orders/order_list.html"
    context_object_name: str = "orders"
    paginate_by: int = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


class OrderDetailView(DetailView):
    """Выводит информацию о конкретном заказе"""
    model = Order
    template_name: str = "orders/order_detail.html"
    context_object_name: str = "order"


class OrderCreateView(CreateView):
    """Создание нового заказа"""
    model = Order
    form_class = OrderForm
    template_name: str = "orders/order_form.html"
    success_url = reverse_lazy("orders:order_list")


class OrderUpdateView(UpdateView):
    """Редактирование заказа"""
    model = Order
    form_class = OrderForm
    template_name: str = "orders/order_form.html"
    success_url = reverse_lazy("orders:order_list")


class OrderDeleteView(DeleteView):
    """Удаление заказа"""
    model = Order
    template_name: str = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("orders:order_list")