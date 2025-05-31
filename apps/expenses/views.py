from django.urls import reverse_lazy
from django.views import generic
from django.utils.decorators import method_decorator

from django.db.models import Q
from .models import ExpenseCategory, Expense
from .forms import ExpenseCategoryForm, ProductForm, ExpenseForm
from apps.users.decorators import role_required
from apps.inventory.models import Category, Product

admin_only = method_decorator(role_required("ADMIN", "SUPERADMIN"), name="dispatch")


@admin_only
class ExpenseCategoryList(generic.ListView):
    model = ExpenseCategory
    template_name = "expenses/category_list.html"


@admin_only
class ExpenseCategoryCreate(generic.CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expenses/category_form.html"
    success_url = reverse_lazy("exp_cat_list")


@admin_only
class ExpenseCategoryUpdate(generic.UpdateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expenses/category_form.html"
    success_url = reverse_lazy("exp_cat_list")


@admin_only
class ExpenseCategoryDelete(generic.DeleteView):
    model = ExpenseCategory
    template_name = "partials/confirm_delete.html"
    success_url = reverse_lazy("exp_cat_list")


# PRODUCT CRUD
@admin_only
class ProductList(generic.ListView):
    model = Product
    template_name = "expenses/product_list.html"


@admin_only
class ProductCreate(generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = "expenses/product_form.html"
    success_url = reverse_lazy("product_list")


@admin_only
class ProductUpdate(generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "expenses/product_form.html"
    success_url = reverse_lazy("product_list")


@admin_only
class ProductDelete(generic.DeleteView):
    model = Product
    template_name = "partials/confirm_delete.html"
    success_url = reverse_lazy("product_list")


@admin_only
class ExpenseList(generic.ListView):
    model = Expense
    template_name = "expenses/expense_list.html"
    context_object_name = "expenses"
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().select_related("category", "product", "user")
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(
                Q(category__name__icontains=q) | Q(product__name__icontains=q)
            )
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


@admin_only
class ExpenseCreate(generic.CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expense_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["products_by_cat"] = {
            str(cat.id): list(Product.objects.filter(category=cat).values("id", "name"))
            for cat in Category.objects.all()
        }
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@admin_only
class ExpenseUpdate(generic.UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expense_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["products_by_cat"] = {
            str(cat.id): list(Product.objects.filter(category=cat).values("id", "name"))
            for cat in Category.objects.all()
        }
        return context


@admin_only
class ExpenseDelete(generic.DeleteView):
    model = Expense
    template_name = "partials/confirm_delete.html"
    success_url = reverse_lazy("expense_list")
