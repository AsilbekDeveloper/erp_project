from django.urls import path
from .views import (
    ProductList,
    ProductCreate,
    ProductUpdate,
    ProductDelete,
    CategoryList,
    CategoryCreate,
    CategoryUpdate,
    CategoryDelete,
    WarehouseList,
    WarehouseCreate,
    WarehouseUpdate,
    WarehouseDelete,
    ajax_add_category,
)


urlpatterns = [
    # Products
    path("", ProductList.as_view(), name="product_list"),
    path("new/", ProductCreate.as_view(), name="product_create"),
    path("<int:pk>/edit/", ProductUpdate.as_view(), name="product_update"),
    path("<int:pk>/del/", ProductDelete.as_view(), name="product_delete"),
    # Categories
    path("categories/", CategoryList.as_view(), name="inv_category_list"),
    path("categories/new/", CategoryCreate.as_view(), name="inv_category_create"),
    path(
        "categories/<int:pk>/edit/",
        CategoryUpdate.as_view(),
        name="inv_category_update",
    ),
    path(
        "categories/<int:pk>/del/", CategoryDelete.as_view(), name="inv_category_delete"
    ),
    # Warehouses
    path("warehouses/", WarehouseList.as_view(), name="warehouse_list"),
    path("warehouses/new/", WarehouseCreate.as_view(), name="warehouse_create"),
    path(
        "warehouses/<int:pk>/edit/", WarehouseUpdate.as_view(), name="warehouse_update"
    ),
    path(
        "warehouses/<int:pk>/del/", WarehouseDelete.as_view(), name="warehouse_delete"
    ),
    # === AJAX uchun category qo‘shish ===
    path("categories/ajax/add/", ajax_add_category, name="ajax_add_category"),
]
