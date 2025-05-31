from django.test import TestCase
from django.db.utils import IntegrityError
from apps.inventory.models import Category, Warehouse, Product, StockMovement
from apps.users.models import User


class CategoryModelTest(TestCase):
    def test_create_and_str(self):
        c = Category.objects.create(name="Electronics")
        self.assertEqual(str(c), "Electronics")

    def test_unique_constraint(self):
        Category.objects.create(name="Shoes")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Shoes")

    def test_long_name(self):
        name = "A" * 120
        c = Category.objects.create(name=name)
        self.assertEqual(c.name, name)


class WarehouseModelTest(TestCase):
    def test_create_and_str(self):
        w = Warehouse.objects.create(name="WH1", address="Main St")
        self.assertEqual(str(w), "WH1")
        self.assertEqual(w.address, "Main St")

    def test_blank_address(self):
        w = Warehouse.objects.create(name="WH2")
        self.assertEqual(w.address, "")

    def test_long_name(self):
        w = Warehouse.objects.create(name="W" * 120)
        self.assertTrue(w.name.startswith("W"))


class ProductModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Food")

    def test_create_and_str(self):
        p = Product.objects.create(
            sku="SKU01", name="Egg", category=self.cat, cost_price=1.5, sell_price=2.2
        )
        self.assertEqual(str(p), f"Egg ({self.cat.name})")

    def test_unique_sku(self):
        Product.objects.create(
            sku="S1", name="Apple", category=self.cat, cost_price=1, sell_price=1
        )
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                sku="S1", name="Banana", category=self.cat, cost_price=2, sell_price=3
            )

    def test_optional_size_color(self):
        p = Product.objects.create(
            sku="S2",
            name="Jacket",
            category=self.cat,
            cost_price=25,
            sell_price=30,
            size="L",
            color="Blue",
        )
        self.assertEqual(p.size, "L")
        self.assertEqual(p.color, "Blue")

    def test_blank_size_color(self):
        p = Product.objects.create(
            sku="S3", name="Shirt", category=self.cat, cost_price=12, sell_price=15
        )
        self.assertEqual(p.size, "")
        self.assertEqual(p.color, "")

    def test_cost_sell_price(self):
        p = Product.objects.create(
            sku="S4", name="Dress", category=self.cat, cost_price=44.4, sell_price=66.6
        )
        self.assertEqual(float(p.cost_price), 44.4)
        self.assertEqual(float(p.sell_price), 66.6)


class StockMovementModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="p")
        self.cat = Category.objects.create(name="Milk")
        self.wh = Warehouse.objects.create(name="Store")
        self.prod = Product.objects.create(
            sku="S5", name="Butter", category=self.cat, cost_price=7, sell_price=8
        )

    def test_create_in(self):
        sm = StockMovement.objects.create(
            product=self.prod,
            warehouse=self.wh,
            user=self.user,
            movement_type="IN",
            quantity=10,
        )
        self.assertEqual(sm.movement_type, "IN")
        self.assertEqual(sm.quantity, 10)

    def test_create_out(self):
        sm = StockMovement.objects.create(
            product=self.prod,
            warehouse=self.wh,
            user=self.user,
            movement_type="OUT",
            quantity=3,
        )
        self.assertEqual(sm.movement_type, "OUT")

    def test_str(self):
        sm = StockMovement.objects.create(
            product=self.prod,
            warehouse=self.wh,
            user=self.user,
            movement_type="IN",
            quantity=6,
        )
        self.assertEqual(str(sm), f"{self.prod} IN 6")

    def test_null_user(self):
        sm = StockMovement.objects.create(
            product=self.prod,
            warehouse=self.wh,
            user=None,
            movement_type="IN",
            quantity=2,
        )
        self.assertIsNone(sm.user)

    def test_quantity(self):
        sm = StockMovement.objects.create(
            product=self.prod,
            warehouse=self.wh,
            user=self.user,
            movement_type="IN",
            quantity=100,
        )
        self.assertEqual(sm.quantity, 100)

    def test_index_exists(self):
        self.assertTrue(
            any(
                idx.fields == ["movement_type", "product"]
                for idx in StockMovement._meta.indexes
            )
        )
