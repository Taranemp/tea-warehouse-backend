from teatracer.models import PickingPeriod

def create_or_link_picking_period(name, start, end, stdout):
    period, created = PickingPeriod.objects.get_or_create(
        name=name,
        defaults={"start_date": start, "end_date": end}
    )
    if created:
        stdout.write(f'PickingPeriod "{name}" created')
    return period


def create_picking_periods(stdout):
    return {
        "spring": create_or_link_picking_period(
            "Spring 2025", "2025-03-01", "2025-05-31", stdout
        ),
        "summer": create_or_link_picking_period(
            "Summer 2025", "2025-06-01", "2025-08-31", stdout
        ),
    }
