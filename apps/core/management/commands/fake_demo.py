# apps/core/management/commands/fake_demo.py
from __future__ import annotations

import random
from decimal import Decimal
from typing import List

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from apps.users.models import User, Role
from apps.inventory.models import Category, Warehouse, Product, StockMovement
from apps.sales.models import Customer, SaleOrder, SaleOrderLine
from apps.expenses.models import Expense, ExpenseCategory

fake = Faker("uz_UZ")
Faker.seed(42)
rnd = random.Random(42)          # deterministik “tasodif”

# ───────────────────────────  STATIK MA’LUMOT ──────────────────────────
UZBEK_CITIES: list[str] = [
    "Toshkent", "Samarqand", "Buxoro", "Andijon", "Farg‘ona", "Namangan",
    "Navoiy", "Qarshi", "Urganch", "Nukus", "Termiz",
]

EXPENSE_CATS = [
    "Ijaraga to‘lov", "Kommunal xizmatlar", "Reklama",
    "Maoshlar", "Transport", "Inventar", "Texnika", "Boshqa"
]

# (qisqartirilgan) Kategoriya → Mahsulot nomlari
CATEGORIES = {
    "Bosh kiyimlar":  ["Shlyapa", "Panama", "Kepka"],
    "Paltolar":       ["Qishki palto", "Trenchcoat"],
    "Kurtkalar":      ["Yomg‘ir kurtkasi", "Bomber"],
    "Kostyumlar":     ["Smoking", "Klassik kostyum"],
    "Poyabzal":       ["Krasovka", "Tufli"],
    "Aksessuarlar":   ["Belbog‘", "Sumka"],
}

SIZES  = ["XS", "S", "M", "L", "XL"]
COLORS = ["Qora", "Oq", "Kulrang", "Bej", "Ko‘k"]

# ─────────────────────────  UTIL FUNKSIYALAR  ──────────────────────────
def even_month_amount(base: int, spread: float = .1) -> int:
    """Bazadan ±spread foiz diapazonda son qaytaradi (grafikni tekislash)."""
    delta = base * spread
    return int(rnd.uniform(base - delta, base + delta))

def reset_db():
    Expense.objects.all().delete()
    ExpenseCategory.objects.all().delete()
    SaleOrderLine.objects.all().delete()
    SaleOrder.objects.all().delete()
    Customer.objects.all().delete()
    StockMovement.objects.all().delete()
    Product.objects.all().delete()
    Warehouse.objects.all().delete()
    Category.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

# ───────────────────────────────  COMMAND  ─────────────────────────────
class Command(BaseCommand):
    help = "ERP MARKET loyihasi uchun balanslangan demo-ma’lumotlar yaratadi"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("→ Demo data tozalanmoqda…"))
        reset_db()

        # 1) Foydalanuvchilar
        staff:   List[User] = [
            User.objects.create_user(
                username=fake.unique.user_name(),
                password="demo1234",
                role=Role.ADMIN if i < 3 else Role.STAFF,
                phone=fake.phone_number(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            ) for i in range(8)
        ]
        if not User.objects.filter(role=Role.SUPERADMIN).exists():
            User.objects.create_superuser(
                username="superadmin",
                password="superadmin123",
                role=Role.SUPERADMIN,
                phone=fake.phone_number(),
                email="admin@erp.uz",
            )

        # 2) Inventory kategoriyalari
        categories = {
            name: Category.objects.create(name=name) for name in CATEGORIES.keys()
        }

        # 3) Omborxonalar
        warehouses = [
            Warehouse.objects.create(
                name=f"{city} omborxonasi", address=fake.address()
            ) for city in rnd.sample(UZBEK_CITIES, 3)
        ]

        # 4) Mahsulotlar
        products: list[Product] = []
        for cat_name, prod_names in CATEGORIES.items():
            cat = categories[cat_name]
            for prod in prod_names:
                cost = rnd.randint(120_000, 220_000)
                products.append(
                    Product.objects.create(
                        sku=fake.unique.bothify("UZ-???-#####"),
                        name=prod,
                        category=cat,
                        cost_price=cost,
                        sell_price=cost + rnd.randint(15_000, 45_000),
                        size=rnd.choice(SIZES),
                        color=rnd.choice(COLORS),
                    )
                )

        # Boshlang‘ich zaxira: har bir mahsulotga bitta “IN”
        for p in products:
            StockMovement.objects.create(
                product=p,
                warehouse=rnd.choice(warehouses),
                user=rnd.choice(staff),
                movement_type="IN",
                quantity=rnd.randint(30, 60),
            )

        # 5) Mijozlar
        customers = [
            Customer.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name(),
                phone=fake.phone_number(), address=fake.address()
            ) for _ in range(40)
        ]

        # 6) Sotuv buyurtmalari (5 yil × 12 oy × 2 order)
        start_year = timezone.now().year - 4
        for y in range(start_year, start_year + 5):
            for m in range(1, 13):
                for _ in range(2):
                    so = SaleOrder.objects.create(
                        customer=rnd.choice(customers),
                        cashier=rnd.choice(staff),
                        note=fake.sentence(nb_words=4),
                        created_at=timezone.datetime(
                            y, m, rnd.randint(2, 26),
                            tzinfo=timezone.get_current_timezone()
                        ),
                    )
                    # har orderga 2 qator
                    for _ in range(2):
                        prod = rnd.choice(products)
                        qty  = rnd.randint(1, 5)
                        SaleOrderLine.objects.create(
                            order=so, product=prod, quantity=qty, price=prod.sell_price
                        )
                        StockMovement.objects.create(
                            product=prod, warehouse=rnd.choice(warehouses),
                            user=rnd.choice(staff), movement_type="OUT", quantity=qty
                        )
        # 7) Xarajat kategoriyalari (ExpenseCategory modeli uchun)
        exp_cats = [ExpenseCategory.objects.create(name=n) for n in EXPENSE_CATS]

        # 8) Xarajatlar (Expense uchun ExpenseCategory ishlatiladi)
        base_month_cost = 120_000
        for y in range(start_year, start_year + 5):
            for m in range(1, 13):
                for _ in range(2):
                    Expense.objects.create(
                        category=rnd.choice(exp_cats),  # ← To‘g‘ri ExpenseCategory ishlatilmoqda
                        product=rnd.choice(products),
                        amount=even_month_amount(base_month_cost, .1),
                        note=fake.sentence(nb_words=3),
                        user=rnd.choice(staff),
                        created_at=timezone.datetime(
                            y, m, rnd.randint(1, 27),
                            tzinfo=timezone.get_current_timezone()
                        )
                    )

        self.stdout.write(self.style.SUCCESS("✓ Balanslangan demo ma’lumotlar tayyor!"))