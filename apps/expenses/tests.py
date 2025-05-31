from django.test import TestCase
from django.db.utils import IntegrityError
from apps.expenses.models import Expense, ExpenseCategory
from apps.inventory.models import Category, Product
from apps.users.models import User


class ExpenseCategoryModelTest(TestCase):
    def test_create_expense_category(self):
        cat = ExpenseCategory.objects.create(name="Transport")
        self.assertEqual(str(cat), "Transport")

    def test_unique_name(self):
        ExpenseCategory.objects.create(name="Internet")
        with self.assertRaises(IntegrityError):
            ExpenseCategory.objects.create(name="Internet")

    def test_long_name(self):
        name = "x" * 120
        cat = ExpenseCategory.objects.create(name=name)
        self.assertEqual(cat.name, name)

    def test_ordering(self):
        a = ExpenseCategory.objects.create(name="A")
        b = ExpenseCategory.objects.create(name="B")
        cats = ExpenseCategory.objects.all()
        self.assertIn(a, cats)
        self.assertIn(b, cats)


class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pw")
        self.exp_cat = ExpenseCategory.objects.create(name="Cat1")
        self.prod_cat = Category.objects.create(name="ProductCat1")
        self.prod = Product.objects.create(
            sku="SKU1", name="P1", category=self.prod_cat, cost_price=10, sell_price=12
        )
        self.cat = self.exp_cat

    def test_create_expense(self):
        exp = Expense.objects.create(
            category=self.exp_cat,  # Use self.exp_cat here
            product=self.prod,
            amount=3.50,
            note="Lunch",
            user=self.user,
        )
        self.assertEqual(exp.note, "Lunch")
        self.assertTrue(str(exp).startswith("Cat1 - P1"))


    def test_null_note(self):
        exp = Expense.objects.create(
            category=self.cat, product=self.prod, amount=1, note="", user=self.user
        )
        self.assertEqual(exp.note, "")

    def test_user_can_be_null(self):
        exp = Expense.objects.create(
            category=self.cat, product=self.prod, amount=1, note="test", user=None
        )
        self.assertIsNone(exp.user)

    def test_amount_decimal(self):
        exp = Expense.objects.create(
            category=self.cat, product=self.prod, amount=5.75, note="d", user=self.user
        )
        self.assertEqual(float(exp.amount), 5.75)

    def test_category_protect(self):
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=2, note="", user=self.user
        )
        with self.assertRaises(Exception):
            self.cat.delete()

    def test_product_protect(self):
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=2, note="", user=self.user
        )
        with self.assertRaises(Exception):
            self.prod.delete()

    def test_multiple_expenses(self):
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=1, note="a", user=self.user
        )
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=2, note="b", user=self.user
        )
        self.assertEqual(Expense.objects.count(), 2)

    def test_amount_limit(self):
        ex = Expense.objects.create(
            category=self.cat,
            product=self.prod,
            amount=999999999.99,
            note="Z",
            user=self.user,
        )
        self.assertEqual(ex.amount, 999999999.99)

    def test_expense_query_by_user(self):
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=5, note="", user=self.user
        )
        self.assertTrue(Expense.objects.filter(user=self.user).exists())

    def test_expense_query_by_category(self):
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=7, note="", user=self.user
        )
        self.assertEqual(Expense.objects.filter(category=self.cat).count(), 1)

    def test_expense_query_by_product(self):
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=2, note="", user=self.user
        )
        self.assertEqual(Expense.objects.filter(product=self.prod).count(), 1)

    def test_expense_query_by_amount(self):
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=22.22, note="", user=self.user
        )
        self.assertTrue(Expense.objects.filter(amount=22.22).exists())

    def test_delete_expense(self):
        ex = Expense.objects.create(
            category=self.cat, product=self.prod, amount=1, note="", user=self.user
        )
        ex.delete()
        self.assertEqual(Expense.objects.count(), 0)

    def test_note_length(self):
        note = "A" * 255
        ex = Expense.objects.create(
            category=self.cat, product=self.prod, amount=3, note=note, user=self.user
        )
        self.assertEqual(ex.note, note)

    def test_blank_note(self):
        ex = Expense.objects.create(
            category=self.cat, product=self.prod, amount=4, note="", user=self.user
        )
        self.assertEqual(ex.note, "")

    def test_max_decimal(self):
        val = 9999999999.99
        ex = Expense.objects.create(
            category=self.cat, product=self.prod, amount=val, note="big", user=self.user
        )
        self.assertEqual(float(ex.amount), val)

    def test_expense_with_different_users(self):
        user2 = User.objects.create_user(username="test2", password="t")
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=1, note="a", user=self.user
        )
        Expense.objects.create(
            category=self.cat, product=self.prod, amount=1, note="b", user=user2
        )
        self.assertEqual(Expense.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Expense.objects.filter(user=user2).count(), 1)

    def test_expense_with_null_category(self):
        with self.assertRaises(Exception):
            Expense.objects.create(
                category=None, product=self.prod, amount=1, note="a", user=self.user
            )

    def test_expense_with_null_product(self):
        with self.assertRaises(Exception):
            Expense.objects.create(
                category=self.cat, product=None, amount=1, note="a", user=self.user
            )

    def test_expense_no_user(self):
        ex = Expense.objects.create(
            category=self.cat, product=self.prod, amount=4.3, note="", user=None
        )
        self.assertIsNone(ex.user)



    def test_expense_with_zero_amount(self):
        ex = Expense.objects.create(
            category=self.cat, product=self.prod, amount=0, note="", user=self.user
        )
        self.assertEqual(ex.amount, 0)
