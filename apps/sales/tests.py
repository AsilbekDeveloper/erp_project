from django.test import TestCase
from apps.sales.models import Customer, SaleOrder, SaleOrderLine
from apps.users.models import User
from apps.inventory.models import Product, Category


class CustomerModelTest(TestCase):
    def test_create_customer(self):
        c = Customer.objects.create(
            first_name="Ali",
            last_name="Valiyev",
            phone="998901234567",
            address="Tashkent",
        )
        self.assertEqual(str(c), "Ali Valiyev")
        self.assertEqual(c.phone, "998901234567")
        self.assertEqual(c.address, "Tashkent")

    def test_blank_last_name(self):
        c = Customer.objects.create(
            first_name="Ali", last_name="", phone="", address=""
        )
        self.assertEqual(str(c), "Ali")

    def test_max_lengths(self):
        fn = "A" * 60
        ln = "B" * 60
        addr = "C" * 255
        c = Customer.objects.create(
            first_name=fn, last_name=ln, phone="1", address=addr
        )
        self.assertEqual(c.first_name, fn)
        self.assertEqual(c.last_name, ln)
        self.assertEqual(c.address, addr)

    def test_create_multiple_customers(self):
        Customer.objects.create(first_name="A", last_name="B")
        Customer.objects.create(first_name="C", last_name="D")
        self.assertEqual(Customer.objects.count(), 2)

    def test_customer_strips(self):
        c = Customer.objects.create(first_name="Q", last_name="")
        self.assertEqual(str(c), "Q")

    def test_blank_fields(self):
        c = Customer.objects.create(first_name="D", last_name="", phone="", address="")
        self.assertEqual(c.phone, "")
        self.assertEqual(c.address, "")


class SaleOrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cash", password="pw")
        self.customer = Customer.objects.create(first_name="Ali", last_name="Valiyev")
        self.cat = Category.objects.create(name="Cat")
        self.product = Product.objects.create(
            sku="111", name="Product1", category=self.cat, cost_price=1, sell_price=2
        )

    def test_create_sale_order(self):
        so = SaleOrder.objects.create(
            customer=self.customer, cashier=self.user, note="test"
        )
        self.assertEqual(str(so), f"SO-{so.pk}")
        self.assertEqual(so.note, "test")

    def test_null_customer(self):
        so = SaleOrder.objects.create(customer=None, cashier=self.user, note="")
        self.assertIsNone(so.customer)

    def test_null_cashier(self):
        so = SaleOrder.objects.create(customer=self.customer, cashier=None, note="")
        self.assertIsNone(so.cashier)

    def test_blank_note(self):
        so = SaleOrder.objects.create(
            customer=self.customer, cashier=self.user, note=""
        )
        self.assertEqual(so.note, "")

    def test_add_lines_and_total(self):
        so = SaleOrder.objects.create(customer=self.customer, cashier=self.user)
        SaleOrderLine.objects.create(
            order=so, product=self.product, quantity=2, price=100
        )
        SaleOrderLine.objects.create(
            order=so, product=self.product, quantity=3, price=200
        )
        self.assertEqual(so.lines.count(), 2)
        self.assertEqual(so.total, 2 * 100 + 3 * 200)

    def test_total_zero_if_no_lines(self):
        so = SaleOrder.objects.create(customer=self.customer, cashier=self.user)
        self.assertEqual(so.total, 0)

    def test_delete_sale_order(self):
        so = SaleOrder.objects.create(customer=self.customer, cashier=self.user)
        so.delete()
        self.assertEqual(SaleOrder.objects.count(), 0)

    def test_multiple_orders(self):
        so1 = SaleOrder.objects.create(customer=self.customer, cashier=self.user)
        so2 = SaleOrder.objects.create(customer=self.customer, cashier=self.user)
        self.assertEqual(SaleOrder.objects.count(), 2)

    def test_lines_related_name(self):
        so = SaleOrder.objects.create(customer=self.customer, cashier=self.user)
        line = SaleOrderLine.objects.create(
            order=so, product=self.product, quantity=1, price=10
        )
        self.assertEqual(so.lines.first(), line)

    def test_update_note(self):
        so = SaleOrder.objects.create(
            customer=self.customer, cashier=self.user, note="old"
        )
        so.note = "new"
        so.save()
        self.assertEqual(SaleOrder.objects.get(pk=so.pk).note, "new")


class SaleOrderLineModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pw")
        self.customer = Customer.objects.create(first_name="Ali", last_name="Valiyev")
        self.cat = Category.objects.create(name="Cat")
        self.product = Product.objects.create(
            sku="123", name="Milk", category=self.cat, cost_price=3, sell_price=4
        )
        self.order = SaleOrder.objects.create(customer=self.customer, cashier=self.user)

    def test_create_sale_order_line(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=5, price=2.50
        )
        self.assertEqual(line.subtotal, 5 * 2.50)

    def test_str_method(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=3, price=1.50
        )
        self.assertEqual(line.subtotal, 4.5)

    def test_delete_line(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=2, price=3
        )
        pk = line.pk
        line.delete()
        self.assertFalse(SaleOrderLine.objects.filter(pk=pk).exists())

    def test_product_protect(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=1, price=1
        )
        with self.assertRaises(Exception):
            self.product.delete()

    def test_foreign_key_to_order(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=1, price=2
        )
        self.assertEqual(line.order, self.order)

    def test_foreign_key_to_product(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=1, price=2
        )
        self.assertEqual(line.product, self.product)

    def test_quantity(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=10, price=2
        )
        self.assertEqual(line.quantity, 10)

    def test_price(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=2, price=5.75
        )
        self.assertEqual(float(line.price), 5.75)

    def test_many_lines_on_one_order(self):
        line1 = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=2, price=2
        )
        line2 = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=3, price=3
        )
        self.assertEqual(self.order.lines.count(), 2)

    def test_zero_quantity(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=0, price=1.25
        )
        self.assertEqual(line.quantity, 0)

    def test_zero_price(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=1, price=0
        )
        self.assertEqual(line.price, 0)

    def test_update_quantity(self):
        line = SaleOrderLine.objects.create(
            order=self.order, product=self.product, quantity=1, price=1
        )
        line.quantity = 11
        line.save()
        self.assertEqual(SaleOrderLine.objects.get(pk=line.pk).quantity, 11)
