from django.core.management.base import BaseCommand
from teatracer.management.commands.seed_helpers import (
    create_currencies,
    remove_and_migrate_db,
    create_super_user,
    create_units,
    create_product_types,
    create_products,
    create_providers,
    create_takers,
    create_rooms,
    create_picking_periods,
    create_movement_types,
    create_transactions,
)

class Command(BaseCommand):
    help = "Seed TeaTracer project data"

    def handle(self, *args, **kwargs):
        ctx = {}

        # remove old database, create superuser
        remove_and_migrate_db(self.stdout)
        create_super_user(self.stdout)

        providers_dict = {'IRR': 1, 'USD': 10}
        ctx["currencies"] = create_currencies(providers_dict, self.stdout)

        # units and periods
        ctx["units"] = create_units(self.stdout)
        ctx["picking_periods"] = create_picking_periods(self.stdout)

        # products
        product_types_list = ["green tea", "black tea", "gold tea"]
        ctx["product_types"] = create_product_types(product_types_list, self.stdout)
        ctx["products"] = create_products(ctx["product_types"], self.stdout)

        # providers
        providers_list = ['Provider 1', 'Provider 2', 'Provider 3']
        ctx["providers"] = create_providers(providers_list, self.stdout)


        # takers
        takers_list = ['Taker 1', 'Taker 2', 'Taker 3']
        ctx["takers"] = create_takers(takers_list, self.stdout)


        # rooms
        rooms_list = ["Intake Room", "Process Room", "Processed Stock Room", "Sorting Room", "Mixing Room", "Packaging Room"]
        ctx["rooms"] = create_rooms(rooms_list, self.stdout)


        # movement_types
        movement_types_list = "Inbound", "Outbound", "Internal Transfer", "Process", "MixSort"
        ctx["movement_types"] = create_movement_types(movement_types_list, self.stdout)

        create_transactions(ctx, self.stdout)
