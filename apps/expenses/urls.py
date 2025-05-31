from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.ExpenseCategoryList.as_view(), name="exp_cat_list"),
    path(
        "categories/new/", views.ExpenseCategoryCreate.as_view(), name="exp_cat_create"
    ),
    path(
        "categories/<int:pk>/edit/",
        views.ExpenseCategoryUpdate.as_view(),
        name="exp_cat_update",
    ),
    path(
        "categories/<int:pk>/del/",
        views.ExpenseCategoryDelete.as_view(),
        name="exp_cat_delete",
    ),
    path("", views.ExpenseList.as_view(), name="expense_list"),
    path("new/", views.ExpenseCreate.as_view(), name="expense_create"),
    # QUYIDAGILARNI QO‘SH:
    path("<int:pk>/edit/", views.ExpenseUpdate.as_view(), name="expense_edit"),
    path("<int:pk>/delete/", views.ExpenseDelete.as_view(), name="expense_delete"),
]
