from django.urls import path
from . import views

urlpatterns = [
    path("", views.reports_overview, name="reports_overview"),
    path("sales-csv/", views.sales_csv, name="report_sales_csv"),
]
