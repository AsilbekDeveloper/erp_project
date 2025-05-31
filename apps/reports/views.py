import csv
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render

from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from apps.sales.models import SaleOrderLine
from apps.expenses.models import Expense
from apps.users.decorators import role_required
from django.db.models.functions import TruncMonth, ExtractYear


@role_required("ADMIN", "SUPERADMIN")
def sales_csv(request):
    today = timezone.now().strftime("%Y%m%d")
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="sales_{today}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Product", "Qty", "Price", "Subtotal"])

    lines = SaleOrderLine.objects.select_related("order", "product").order_by(
        "-order__created_at"
    )[:5000]
    for line in lines:
        writer.writerow(
            [
                line.order.created_at.strftime("%Y-%m-%d"),
                line.product.name,
                line.quantity,
                line.price,
                line.subtotal,
            ]
        )
    return response


@role_required("ADMIN", "SUPERADMIN")
def reports_overview(request):
    total_sales = (
        SaleOrderLine.objects.annotate(
            subtotal=ExpressionWrapper(
                F("quantity") * F("price"), output_field=DecimalField()
            )
        ).aggregate(sales=Sum("subtotal"))["sales"]
        or 0
    )
    order_count = SaleOrderLine.objects.values("order").distinct().count()

    current_year = timezone.now().year

    monthly_raw = (
        SaleOrderLine.objects.filter(order__created_at__year=current_year)
        .annotate(month=TruncMonth("order__created_at"))
        .annotate(
            subtotal=ExpressionWrapper(
                F("quantity") * F("price"), output_field=DecimalField()
            )
        )
        .values("month")
        .annotate(sum=Sum("subtotal"))
        .order_by("month")
    )
    monthly_data = []
    month_map = {r["month"].month: float(r["sum"]) for r in monthly_raw if r["month"]}
    for m in range(1, 13):
        monthly_data.append(month_map.get(m, 0))

    yearly_raw = (
        SaleOrderLine.objects.annotate(year=ExtractYear("order__created_at"))
        .annotate(
            subtotal=ExpressionWrapper(
                F("quantity") * F("price"), output_field=DecimalField()
            )
        )
        .values("year")
        .annotate(sum=Sum("subtotal"))
        .order_by("year")
    )
    years = [r["year"] for r in yearly_raw]
    yearly_data = [float(r["sum"]) for r in yearly_raw]

    monthly_expenses_raw = (
        Expense.objects.filter(created_at__year=current_year)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(sum=Sum("amount"))
        .order_by("month")
    )
    monthly_expense_map = {
        r["month"].month: float(r["sum"]) for r in monthly_expenses_raw if r["month"]
    }
    monthly_expenses_data = [monthly_expense_map.get(m, 0) for m in range(1, 13)]

    yearly_expenses_raw = (
        Expense.objects.annotate(year=ExtractYear("created_at"))
        .values("year")
        .annotate(sum=Sum("amount"))
        .order_by("year")
    )
    year_expense_map = {
        r["year"]: float(r["sum"]) for r in yearly_expenses_raw if r["year"]
    }
    yearly_expenses_data = [year_expense_map.get(y, 0) for y in years]

    context = {
        "total_sales": total_sales,
        "order_count": order_count,
        "monthly_data": monthly_data,
        "yearly_labels": years,
        "yearly_data": yearly_data,
        "monthly_expenses_data": monthly_expenses_data,
        "yearly_expenses_data": yearly_expenses_data,
        "now": timezone.now(),
    }
    return render(request, "reports/report_overview.html", context)
