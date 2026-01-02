from decimal import Decimal
from teatracer.models import Unit

def create_or_link_unit(name, conversion_to_kg, stdout):
    unit, created = Unit.objects.get_or_create(
        name=name,
        defaults={"conversion_to_kg": conversion_to_kg}
    )
    if created:
        stdout.write(f'Unit "{name}" created')
    else:
        stdout.write(f'Unit "{name}" already exists')
    return unit


def create_units(stdout):
    return {
        "kg": create_or_link_unit("Kilogram", Decimal("1"), stdout),
    }
