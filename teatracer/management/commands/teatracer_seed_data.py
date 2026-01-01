from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal

from teatracer.models import (
    Unit,
    ProductType,
    Product,
    Provider,
    Taker,
    Room,
    PickingPeriod,
    MovementType,
    Transaction
)


class Command(BaseCommand):
    help = "Seed initial data for TeaTracer project"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding data started..."))

        # ---------- Units ----------
        kg, _ = Unit.objects.get_or_create(
            name="Kilogram",
            defaults={"conversion_to_kg": Decimal("1")}
        )

        gram, _ = Unit.objects.get_or_create(
            name="Gram",
            defaults={"conversion_to_kg": Decimal("0.001")}
        )

        # ---------- Product Types ----------
        green_type, _ = ProductType.objects.get_or_create(name="Green Tea")
        black_type, _ = ProductType.objects.get_or_create(name="Black Tea")
        
        # ---------- Products ----------
        premium, _ = Product.objects.get_or_create(
            name="Premium",
            sku="GT-001",
            product_type=black_type,
            defaults={"is_final": False}
        )

        first_flush, _ = Product.objects.get_or_create(
            name="First Flush",
            sku="BT-001",
            product_type=black_type,
            defaults={"is_final": False}
        )
        broken_tea, _ = Product.objects.get_or_create(
            name="Broken Tea",
            sku="BT-002",
            product_type=black_type,
            defaults={"is_final": False}
        )
        long_leaf, _ = Product.objects.get_or_create(
            name="Long Leaf",
            sku="BT-003",
            product_type=black_type,
            defaults={"is_final": False}
        )
        green_tea_A, _ = Product.objects.get_or_create(
            name="Green Tea A",
            sku="GT-002",
            product_type=green_type,
            defaults={"is_final": False}
        )

        # ---------- Providers ----------
        provider1, _ = Provider.objects.get_or_create(name="provider 1")
        provider2, _ = Provider.objects.get_or_create(name="provider 2")
        provider2, _ = Provider.objects.get_or_create(name="provider 3")

        # ---------- Takers ----------
        taker1, _ = Taker.objects.get_or_create(name="Taker 1")
        taker2, _ = Taker.objects.get_or_create(name="Taker 2")
        taker2, _ = Taker.objects.get_or_create(name="Taker 3")

        # ---------- Rooms ----------
        withering_room, _ = Room.objects.get_or_create(name="Withering Room")
        rolling_room, _ = Room.objects.get_or_create(name="Rolling Room")
        oxidation_room, _ = Room.objects.get_or_create(name="Oxidation Room")
        drying_room, _ = Room.objects.get_or_create(name="Drying Room")
        sorting_room, _ = Room.objects.get_or_create(name="Sorting Room")
        packaging_room, _ = Room.objects.get_or_create(name="Packaging Room")

        # ---------- Picking Period ----------
        spring_period, _ = PickingPeriod.objects.get_or_create(
            name="Spring 2025",
            defaults={
                "start_date": "2025-03-01",
                "end_date": "2025-05-31"
            }
        )
        summer_period, _ = PickingPeriod.objects.get_or_create(
            name="Summer 2025",
            defaults={
                "start_date": "2025-06-01",
                "end_date": "2025-08-31"
            }
        )

        # ---------- Movement Types ----------
        inbound, _ = MovementType.objects.get_or_create(name="InBound")
        internal_transfer, _ = MovementType.objects.get_or_create(name="Internal Transfer")
        production_consume, _ = MovementType.objects.get_or_create(name="Production Consume")
        production_output, _ = MovementType.objects.get_or_create(name="Production Output")
        sale, _ = MovementType.objects.get_or_create(name="Sale")

        # ---------- Transactions ----------
        Transaction.objects.get_or_create(
            product=premium,
            producttype=black_type,
            quantity=Decimal("100"),
            quantity_in_kg=Decimal("100"),
            unit=kg,
            date=timezone.now().date(),
            from_provider=provider1,
            from_room=sorting_room,
            to_room=packaging_room,
            movement_type=production_output,
            unit_price= Decimal("3000000"),
            currency="IRR",
            picking_period= spring_period
        )

        Transaction.objects.get_or_create(
            product=first_flush,
            producttype=black_type,
            quantity=Decimal("50"),
            quantity_in_kg=Decimal("50"),
            unit=kg,
            date=timezone.now().date(),
            from_room=withering_room,
            to_room=rolling_room,
            movement_type=internal_transfer,
            currency="IRR"
        )

        self.stdout.write(self.style.SUCCESS("Seeding data finished successfully."))
