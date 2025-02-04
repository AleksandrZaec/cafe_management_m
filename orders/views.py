from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from orders.models import Order, OrderItem
from orders.forms import OrderForm, OrderItemForm
from orders.services import calculate_order_total, get_daily_revenue


class OrderListView(ListView):
    """Выводит список заказов с возможностью фильтрации и пагинации"""
    model = Order
    template_name: str = "orders/order_list.html"
    context_object_name: str = "orders"
    paginate_by: int = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


class OrderDetailView(DetailView):
    """Выводит информацию о конкретном заказе с блюдами"""
    model = Order
    template_name: str = "orders/order_detail.html"
    context_object_name: str = "order"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["items"] = self.object.items.all()
        return context


class OrderCreateView(CreateView):
    """Создание нового заказа с блюдами"""
    model = Order
    form_class = OrderForm
    template_name: str = "orders/order_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("orders:order_list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True)

        if self.request.method == "POST":
            context_data["formset"] = OrderFormset(self.request.POST)
        else:
            context_data["formset"] = OrderFormset()

        return context_data

    def form_valid(self, form: OrderForm) -> Any:
        context_data = self.get_context_data()
        formset = context_data["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            total_price = calculate_order_total(self.object)
            self.object.total_price = total_price
            self.object.save()

            return super().form_valid(form)

        return self.render_to_response(context_data)


class OrderUpdateView(UpdateView):
    """Редактирование заказа"""
    model = Order
    form_class = OrderForm
    template_name: str = "orders/order_form.html"

    def get_success_url(self) -> str:
        return reverse('orders:order_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        OrderFormset = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True)

        if self.request.method == 'POST':
            context_data["formset"] = OrderFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = OrderFormset(instance=self.object)

        return context_data

    def form_valid(self, form: OrderForm) -> Any:
        context_data = self.get_context_data()
        formset = context_data["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            total_price = calculate_order_total(self.object)
            self.object.total_price = total_price
            self.object.save()

            return super().form_valid(form)

        return self.render_to_response(context_data)


class OrderDeleteView(DeleteView):
    """Удаление заказа"""
    model = Order
    template_name: str = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("orders:order_list")


def revenue_view(request) -> Any:
    """Выводит общую выручку за сегодняшний день"""
    today = timezone.now().date()
    total_revenue = get_daily_revenue()
    return render(request, 'orders/daily_revenue.html', {
        'total_revenue': total_revenue,
        'today': today
    })
