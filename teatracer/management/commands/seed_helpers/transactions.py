from decimal import Decimal
from django.utils import timezone
from teatracer.models import Transaction

def create_transactions(ctx, stdout):
    today = timezone.now().date()

    # ----------------------------
    # Inbound
    # ----------------------------
    inbound_data = [
        ("Leaf G1", "Provider 1", "Intake Room", 100),
        ("Leaf G2", "Provider 2", "Intake Room", 80),
        ("Leaf G3", "Provider 3", "Intake Room", 50),
    ]
    for product_key, provider_key, room_key, qty in inbound_data:
        Transaction.objects.get_or_create(
            product=ctx["products"][product_key],
            quantity=Decimal(qty),
            quantity_in_kg=Decimal(qty),
            unit=ctx["units"]["kg"],
            date=today,
            from_provider=ctx["providers"][provider_key],
            from_room=None,
            to_room=ctx["rooms"][room_key],
            movement_type=ctx["movement_types"]["Inbound"],
            unit_price=Decimal("300"),
            currency=ctx["currencies"]["IRR"],
            picking_period=ctx["picking_periods"]["spring"],
        )

    # ----------------------------
    # Internal Transfer
    # ----------------------------
    internal_moves = [
        # Process Room
        ("Leaf G1", "Intake Room", "Process Room", 60),
        ("Leaf G2", "Intake Room", "Process Room", 50),
        # Processed Stock Room
        ("Processed leaf", "Process Room", "Processed Stock Room", 80),
        # Sorting Room
        ("Sort A", "Processed Stock Room", "Sorting Room", 30),
        ("Sort B", "Processed Stock Room", "Sorting Room", 20),
        ("Sort C", "Processed Stock Room", "Sorting Room", 15),
        # Mixing Room
        ("Mix Tea AB", "Sorting Room", "Mixing Room", 25),
        ("Mix Tea CD", "Sorting Room", "Mixing Room", 20),
        # Packaging Room
        ("Mix Tea FE", "Mixing Room", "Packaging Room", 30),
    ]
    for product_key, from_room_key, to_room_key, qty in internal_moves:
        Transaction.objects.get_or_create(
            product=ctx["products"][product_key],
            quantity=Decimal(qty),
            quantity_in_kg=Decimal(qty),
            unit=ctx["units"]["kg"],
            date=today,
            from_room=ctx["rooms"][from_room_key],
            to_room=ctx["rooms"][to_room_key],
            movement_type=ctx["movement_types"]["Internal Transfer"],
            currency=ctx["currencies"]["IRR"],
        )

    # ----------------------------
    # Outbound
    # ----------------------------
    outbound_data = [
        ("Mix Tea AB", "Packaging Room", None, 10),
        ("Mix Tea FE", "Packaging Room", None, 5),
    ]
    for product_key, from_room_key, to_taker_key, qty in outbound_data:
        Transaction.objects.get_or_create(
            product=ctx["products"][product_key],
            quantity=Decimal(qty),
            quantity_in_kg=Decimal(qty),
            unit=ctx["units"]["kg"],
            date=today,
            from_room=ctx["rooms"][from_room_key],
            to_taker=ctx["takers"].get(to_taker_key, None),
            to_room=None,
            movement_type=ctx["movement_types"]["Outbound"],
            currency=ctx["currencies"]["IRR"],
        )

    stdout.write("Transactions seeded successfully")
