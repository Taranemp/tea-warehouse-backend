from django.contrib import admin
from .models import (
    Unit,
    ProductType,
    Product,
    Provider,
    Taker,
    Room,
    PickingPeriod,
    MovementType,
    Transaction,
)
admin.site.register(Unit)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Provider)
admin.site.register(Taker)
admin.site.register(Room)
admin.site.register(PickingPeriod)
admin.site.register(MovementType)
admin.site.register(Transaction)

