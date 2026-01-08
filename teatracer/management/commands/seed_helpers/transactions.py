from decimal import Decimal
from django.utils import timezone
from teatracer.models import Transaction, AddedProduct, RemovedProduct

def create_transactions(ctx, stdout):
    today = timezone.now().date()
    kg_unit = ctx["units"]["kg"]

    # ----------------------------
    # INBOUND (Provider -> Room)
    # ----------------------------
    inbound_data = [
        ("Leaf G1", "Provider 1", "Intake Room", 100),
        ("Leaf G2", "Provider 2", "Intake Room", 200),
        ("Leaf G3", "Provider 3", "Intake Room", 300),
    ]

    for product_key, provider_key, to_room, qty in inbound_data:
        transaction = Transaction.objects.create(
            transaction_type=ctx["transaction_types"]["Intake"],
            date=today,
            notes=f"Inbound from {provider_key}",
            picking_period=ctx["picking_periods"]["spring"],
        )

        quantity = Decimal(qty)
        AddedProduct.objects.create(
            transaction=transaction,
            product=ctx["products"][product_key],
            quantity=quantity,
            unit=kg_unit,
            quantity_in_kg=quantity * kg_unit.conversion_to_kg,
            from_room=None,
            to_room=ctx["rooms"][to_room],
            provider=ctx["providers"][provider_key],
            taker=None,
            notes="Initial inbound",
        )

    # ----------------------------
    # MIXING / INSIDE ( room input -> same room + other room output)
    # ----------------------------
    mixing_transaction = Transaction.objects.create(
        date=today,
        transaction_type=ctx["transaction_types"]["Mixing"],
        notes="Mix G1+G2+G3 into Mix Leaf to partially Transfer to the process room",
        picking_period=ctx["picking_periods"]["spring"],
    )

    # remove individual leafs from room
    RemovedProduct.objects.create(
        transaction=mixing_transaction,
        product=ctx["products"]["Leaf G1"],
        quantity=Decimal(50),
        unit=kg_unit,
        quantity_in_kg=Decimal(50) * kg_unit.conversion_to_kg,
        to_room=ctx["rooms"]["Intake Room"],
        from_room=ctx["rooms"]["Intake Room"],
        provider=None,
        taker=None,
        notes="Used in mixing",
    )
    RemovedProduct.objects.create(
        transaction=mixing_transaction,
        product=ctx["products"]["Leaf G2"],
        quantity=Decimal(100),
        unit=kg_unit,
        quantity_in_kg=Decimal(100) * kg_unit.conversion_to_kg,
        to_room=ctx["rooms"]["Intake Room"],
        from_room=ctx["rooms"]["Intake Room"],
        provider=None,
        taker=None,
        notes="Used in mixing",
    )
    RemovedProduct.objects.create(
        transaction=mixing_transaction,
        product=ctx["products"]["Leaf G3"],
        quantity=Decimal(150),
        unit=kg_unit,
        quantity_in_kg=Decimal(150) * kg_unit.conversion_to_kg,
        to_room=ctx["rooms"]["Intake Room"],
        from_room=ctx["rooms"]["Intake Room"],
        provider=None,
        taker=None,
        notes="Used in mixing",
    )

    # add mixed product to same room
    AddedProduct.objects.create(
        transaction=mixing_transaction,
        product=ctx["products"]["Mix Leaf"],
        quantity=Decimal(100),
        unit=kg_unit,
        quantity_in_kg=Decimal(100) * kg_unit.conversion_to_kg,
        to_room=ctx["rooms"]["Intake Room"],
        from_room=ctx["rooms"]["Intake Room"],
        provider=None,
        taker=None,
        notes="Result of mixing",
    )
    AddedProduct.objects.create(
        transaction=mixing_transaction,
        product=ctx["products"]["Mix Leaf"],
        quantity=Decimal(200),
        unit=kg_unit,
        quantity_in_kg=Decimal(200) * kg_unit.conversion_to_kg,
        to_room=ctx["rooms"]["Process Room"],
        from_room=ctx["rooms"]["Intake Room"],
        provider=None,
        taker=None,
        notes="Result of mixing",
    )



    # ----------------------------
    # Processing tea
    # ----------------------------
    process_transaction = Transaction.objects.create(
        date=today,
        transaction_type=ctx["transaction_types"]["Processing"],
        notes="Convert 150 kg mix leaf into 100Kg process tea",
        picking_period=ctx["picking_periods"]["spring"],
    )

    # remove from Intake Room
    RemovedProduct.objects.create(
        transaction=process_transaction,
        product=ctx["products"]["Mix Leaf"],
        quantity=Decimal(150),
        unit=kg_unit,
        quantity_in_kg=Decimal(150) * kg_unit.conversion_to_kg,
        from_room=ctx["rooms"]["Process Room"],
        to_room=ctx["rooms"]["Process Room"],
        provider=None,
        taker=None,
        notes="Transferred from Intake Room",
    )

    # add to Process Room
    AddedProduct.objects.create(
        transaction=process_transaction,
        product=ctx["products"]["Processed Leaf"],
        quantity=Decimal(100),
        unit=kg_unit,
        quantity_in_kg=Decimal(100) * kg_unit.conversion_to_kg,
        from_room=ctx["rooms"]["Process Room"],
        to_room=ctx["rooms"]["Process Room"],
        provider=None,
        taker=None,
        notes="Received from Intake Room",
    )

    # ----------------------------
    # Sorting tea
    # ----------------------------
    sorting_transaction = Transaction.objects.create(
        date=today,
        transaction_type=ctx["transaction_types"]["Sorting"],
        notes="transfer 80 kg process tea and sort them into 20kg Sort A, B, C",
        picking_period=ctx["picking_periods"]["spring"],
    )

    # remove from Sorting Room
    RemovedProduct.objects.create(
        transaction=sorting_transaction,
        product=ctx["products"]["Processed Leaf"],
        quantity=Decimal(80),
        unit=kg_unit,
        quantity_in_kg=Decimal(80) * kg_unit.conversion_to_kg,
        from_room=ctx["rooms"]["Process Room"],
        to_room=ctx["rooms"]["Sorting Room"],
        provider=None,
        taker=None,
        notes="Transferred from Process Room int Sorting Room",
    )

    # add to Sorting Room
    AddedProduct.objects.create(
        transaction=sorting_transaction,
        product=ctx["products"]["Sort A"],
        quantity=Decimal(20),
        unit=kg_unit,
        quantity_in_kg=Decimal(20) * kg_unit.conversion_to_kg,
        from_room=ctx["rooms"]["Sorting Room"],
        to_room=ctx["rooms"]["Sorting Room"],
        provider=None,
        taker=None,
        notes="Sort processed tea in Sorting Room for Sort A",
    )

    AddedProduct.objects.create(
        transaction=sorting_transaction,
        product=ctx["products"]["Sort B"],
        quantity=Decimal(40),
        unit=kg_unit,
        quantity_in_kg=Decimal(40) * kg_unit.conversion_to_kg,
        from_room=ctx["rooms"]["Sorting Room"],
        to_room=ctx["rooms"]["Sorting Room"],
        provider=None,
        taker=None,
        notes="Sort processed tea in Sorting Room for Sort B",
    )

    AddedProduct.objects.create(
        transaction=sorting_transaction,
        product=ctx["products"]["Sort C"],
        quantity=Decimal(20),
        unit=kg_unit,
        quantity_in_kg=Decimal(20) * kg_unit.conversion_to_kg,
        from_room=ctx["rooms"]["Sorting Room"],
        to_room=ctx["rooms"]["Sorting Room"],
        provider=None,
        taker=None,
        notes="Sort processed tea in Sorting Room for Sort C",
    )

    stdout.write("Transactions seeded successfully")
