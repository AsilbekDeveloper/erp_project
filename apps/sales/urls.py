from django.urls import path
from . import views

urlpatterns = [
    # Customers
    path("customers/", views.CustomerList.as_view(), name="customer_list"),
    path("customers/new/", views.CustomerCreate.as_view(), name="customer_create"),
    path(
        "customers/<int:pk>/edit/",
        views.CustomerUpdate.as_view(),
        name="customer_update",
    ),
    path(
        "customers/<int:pk>/del/",
        views.CustomerDelete.as_view(),
        name="customer_delete",
    ),
    # Sales Orders
    path("", views.SaleOrderList.as_view(), name="saleorder_list"),
    path("new/", views.SaleOrderCreate.as_view(), name="saleorder_create"),
    path("<int:pk>/", views.SaleOrderDetail.as_view(), name="saleorder_detail"),
    path("<int:pk>/del/", views.SaleOrderDelete.as_view(), name="saleorder_delete"),
    path("customers/ajax/add/", views.ajax_add_customer, name="ajax_add_customer"),
]
