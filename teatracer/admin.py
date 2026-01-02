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

# ----------------------------
# Inlines
# ----------------------------

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    show_change_link = True


# ----------------------------
# ProductType
# ----------------------------

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProductInline]


# ----------------------------
# Product
# ----------------------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sku", "product_type", "is_final", "created_at")
    list_filter = ("product_type", "is_final")
    search_fields = ("name", "sku")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("product_type",)


# ----------------------------
# Unit
# ----------------------------

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "conversion_to_kg", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")


# ----------------------------
# Provider
# ----------------------------

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "created_at")
    search_fields = ("name", "phone")
    readonly_fields = ("created_at", "updated_at")


# ----------------------------
# Taker
# ----------------------------

@admin.register(Taker)
class TakerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "address", "created_at")
    search_fields = ("name", "phone", "address")
    readonly_fields = ("created_at", "updated_at")


# ----------------------------
# Room
# ----------------------------

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")


# ----------------------------
# PickingPeriod
# ----------------------------

@admin.register(PickingPeriod)
class PickingPeriodAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "end_date")
    list_filter = ("start_date", "end_date")
    search_fields = ("name",)
    ordering = ("-start_date",)
    readonly_fields = ("created_at", "updated_at")


# ----------------------------
# MovementType
# ----------------------------

@admin.register(MovementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")


# ----------------------------
# Transaction
# ----------------------------

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    save_on_top = True

    list_display = (
        "id",
        "date",
        "product",
        "movement_type",
        "quantity_display",
        "from_location",
        "to_location",
        "unit_price",
        "total_cost_display",
        "currency",
        "picking_period",
        "created_at",
    )

    list_filter = (
        "movement_type",
        "currency",
        "product",
        "unit",
        "picking_period",
        "from_provider",
        "to_taker",
        "from_room",
        "to_room",
        "date",
    )

    search_fields = (
        "product__name",
        "from_provider__name",
        "to_taker__name",
        "notes",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "quantity_in_kg",
        "total_cost",
    )

    fieldsets = (
        ("Core Information", {
            "fields": ("product", "movement_type", "date", "notes")
        }),
        ("Quantity", {
            "fields": ("quantity", "unit", "quantity_in_kg")
        }),
        ("Locations (Internal)", {
            "fields": ("from_room", "to_room")
        }),
        ("External Parties", {
            "fields": ("from_provider", "to_taker")
        }),
        ("Period & Pricing", {
            "fields": ("picking_period", "unit_price", "total_cost", "currency")
        }),
        ("System Fields", {
            "fields": ("created_at", "updated_at")
        }),
    )

    autocomplete_fields = (
        "product",
        "unit",
        "from_room",
        "to_room",
        "from_provider",
        "to_taker",
        "picking_period",
        "movement_type",
    )

    list_select_related = (
        "product",
        "unit",
        "movement_type",
        "from_room",
        "to_room",
        "from_provider",
        "to_taker",
        "picking_period",
    )

    ordering = ("-date", "-created_at")

    # ----------------------------
    # Display helpers
    # ----------------------------

    @admin.display(description="Quantity")
    def quantity_display(self, obj):
        return f"{obj.quantity} {obj.unit.name}"

    @admin.display(description="From")
    def from_location(self, obj):
        if obj.from_room:
            return f"Room: {obj.from_room.name}"
        if obj.from_provider:
            return f"Provider: {obj.from_provider.name}"
        return "-"

    @admin.display(description="To")
    def to_location(self, obj):
        if obj.to_room:
            return f"Room: {obj.to_room.name}"
        if obj.to_taker:
            return f"Taker: {obj.to_taker.name}"
        return "-"

    @admin.display(description="Total Cost")
    def total_cost_display(self, obj):
        if obj.total_cost:
            return f"{obj.total_cost} {obj.currency}"
        return "-"

    # ----------------------------
    # Auto calculations
    # ----------------------------

    def save_model(self, request, obj, form, change):
        if obj.unit and obj.quantity:
            obj.quantity_in_kg = obj.quantity * obj.unit.conversion_to_kg
        if obj.unit_price:
            obj.total_cost = obj.unit_price * obj.quantity
        super().save_model(request, obj, form, change)
