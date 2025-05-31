from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.db.models import Q
import json

from apps.inventory.models import Product, Category
from apps.users.decorators import role_required
from .models import Customer, SaleOrder
from .forms import CustomerForm, SaleOrderForm, SaleLineFormSet

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

admin_only = method_decorator(role_required("ADMIN", "SUPERADMIN"), name="dispatch")
admin_and_staff = method_decorator(
    role_required("ADMIN", "SUPERADMIN", "STAFF"), name="dispatch"
)


@admin_only
class CustomerList(generic.ListView):
    model = Customer
    template_name = "sales/customer_list.html"


@admin_only
class CustomerCreate(generic.CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "sales/customer_form.html"
    success_url = reverse_lazy("customer_list")


@admin_only
class CustomerUpdate(generic.UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "sales/customer_form.html"
    success_url = reverse_lazy("customer_list")


@admin_only
class CustomerDelete(generic.DeleteView):
    model = Customer
    template_name = "partials/confirm_delete.html"
    success_url = reverse_lazy("customer_list")


@admin_and_staff
class SaleOrderList(generic.ListView):
    model = SaleOrder
    template_name = "sales/saleorder_list.html"

    def get_queryset(self):
        qs = super().get_queryset().select_related("customer", "cashier")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(customer__first_name__icontains=q)
                | Q(customer__last_name__icontains=q)
                | Q(customer__phone__icontains=q)
                | Q(note__icontains=q)
            )
        return qs


@admin_and_staff
class SaleOrderDetail(generic.DetailView):
    model = SaleOrder
    template_name = "sales/saleorder_detail.html"
    context_object_name = "order"


@admin_and_staff
class SaleOrderDelete(generic.DeleteView):
    model = SaleOrder
    template_name = "partials/confirm_delete.html"
    success_url = reverse_lazy("saleorder_list")


class _SaleOrderMixin(View):
    template_name = "sales/saleorder_form.html"
    form_prefix = "lines"

    def _ctx(self, order_form, formset, **extra):
        ctx = {
            "form": order_form,
            "formset": formset,
            "products": Product.objects.all(),
        }
        ctx.update(extra)
        return ctx

    def _bind_formset(self, *args, **kwargs):
        return SaleLineFormSet(*args, prefix=self.form_prefix, **kwargs)

    def _apply_prices(self, formset):
        for form in formset:
            if form.cleaned_data.get("product") and not form.cleaned_data.get("DELETE"):
                form.instance.price = form.cleaned_data["product"].sell_price


@admin_and_staff
class SaleOrderCreate(View):
    template_name = "sales/saleorder_form.html"
    form_prefix = "lines"

    def _ctx(self, order_form, formset, **extra):
        ctx = {
            "form": order_form,
            "formset": formset,
            "products": Product.objects.all(),
        }
        ctx.update(extra)
        return ctx

    def _bind_formset(self, *args, **kwargs):
        return SaleLineFormSet(*args, prefix=self.form_prefix, **kwargs)

    def _apply_prices(self, formset):
        for form in formset:
            if form.cleaned_data.get("product") and not form.cleaned_data.get("DELETE"):
                form.instance.price = form.cleaned_data["product"].sell_price

    def get(self, request):
        categories = Category.objects.all().values("id", "name")
        products = [
            {
                "id": p.id,
                "name": p.name,
                "category_id": p.category_id,
                "sell_price": float(p.sell_price) if p.sell_price is not None else 0,
            }
            for p in Product.objects.all()
        ]
        context = self._ctx(SaleOrderForm(), self._bind_formset())
        context["categories_json"] = json.dumps(list(categories))
        context["products_json"] = json.dumps(list(products))
        context["customers"] = Customer.objects.all()
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        print("POST REQUEST:", request.POST.dict())
        order_form = SaleOrderForm(request.POST)
        formset = self._bind_formset(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.cashier = request.user
            order.save()
            self._apply_prices(formset)
            formset.instance = order
            formset.save()
            return redirect("saleorder_detail", pk=order.pk)
        print("Order Form Errors:", order_form.errors)
        print("Formset Errors:", formset.errors)
        categories = Category.objects.all().values("id", "name")
        products = [
            {
                "id": p.id,
                "name": p.name,
                "category_id": p.category_id,
                "sell_price": float(p.sell_price) if p.sell_price is not None else 0,
            }
            for p in Product.objects.all()
        ]
        context = self._ctx(order_form, formset)
        context["categories_json"] = json.dumps(list(categories))
        context["products_json"] = json.dumps(list(products))
        context["customers"] = Customer.objects.all()
        return render(request, self.template_name, context)


@csrf_exempt
def ajax_add_customer(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        if not first_name:
            return JsonResponse(
                {"success": False, "error": "First name required"}, status=400
            )
        cust = Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
        )
        return JsonResponse(
            {
                "success": True,
                "id": cust.id,
                "name": f"{cust.first_name} {cust.last_name}".strip(),
            }
        )
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
