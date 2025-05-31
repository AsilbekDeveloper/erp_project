import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F, Sum, Case, When, IntegerField
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from .forms import StatsFilterForm
from apps.inventory.models import Product, StockMovement
from apps.sales.models import SaleOrderLine
from apps.expenses.models import Expense


def _to_float(seq):
    return [float(x or 0) for x in seq]


@login_required
def home(request):
    form = StatsFilterForm(request.GET or None)
    year = int(form["year"].value() or datetime.today().year)

    # KPI-lar
    product_cnt = Product.objects.count()
    stock_qty = (
        StockMovement.objects.annotate(
            sign=Case(
                When(movement_type=StockMovement.Type.IN, then=1),
                When(movement_type=StockMovement.Type.OUT, then=-1),
                default=0,
                output_field=IntegerField(),
            )
        ).aggregate(total=Sum(F("quantity") * F("sign")))["total"]
        or 0
    )
    year_total_sales = (
        SaleOrderLine.objects.filter(order__created_at__year=year).aggregate(
            qty=Sum("quantity")
        )["qty"]
        or 0
    )

    pie_qs = (
        SaleOrderLine.objects.filter(order__created_at__year=year)
        .values(cat_name=F("product__category__name"))
        .annotate(qty=Sum("quantity"))
        .order_by("-qty")
    )
    pie_labels = [r["cat_name"] for r in pie_qs]
    pie_data = _to_float([r["qty"] for r in pie_qs])

    sales_qs = (
        SaleOrderLine.objects.filter(order__created_at__year=year)
        .annotate(month=TruncMonth("order__created_at"))
        .values("month")
        .annotate(revenue=Sum(F("quantity") * F("price")))
        .order_by("month")
    )
    exp_qs = (
        Expense.objects.filter(created_at__year=year)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(cost=Sum("amount"))
        .order_by("month")
    )

    months = [datetime(year, m, 1).strftime("%b") for m in range(1, 13)]
    revenue_map = {r["month"].month: r["revenue"] for r in sales_qs if r["month"]}
    cost_map = {e["month"].month: e["cost"] for e in exp_qs if e["month"]}

    bar_revenue = _to_float([revenue_map.get(m, 0) for m in range(1, 13)])
    bar_cost = _to_float([cost_map.get(m, 0) for m in range(1, 13)])
    line_profit = [bar_revenue[i] - bar_cost[i] for i in range(12)]

    ctx = {
        "product_cnt": product_cnt,
        "stock": stock_qty,
        "year_total_sales": int(year_total_sales),
        "year": year,
        "filter_form": form,
        "pie_labels": json.dumps(pie_labels, cls=DjangoJSONEncoder),
        "pie_data": json.dumps(pie_data, cls=DjangoJSONEncoder),
        "months": json.dumps(months, cls=DjangoJSONEncoder),
        "bar_rev": json.dumps(bar_revenue),
        "bar_cost": json.dumps(bar_cost),
        "line_profit": json.dumps(line_profit),
    }
    return render(request, "dashboard/index.html", ctx)
