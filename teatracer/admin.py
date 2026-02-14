from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import (
    Currency,
    PickingPeriod,
    ProductType,
    Product,
    Provider,
    Room,
    Taker,
    Transaction,
    AddedProduct,
    RemovedProduct,
    Unit,
    TransactionType,
    UserProfile,
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
# Currency
# ----------------------------

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ratio", "created_at")
    ordering = ("id",)
    readonly_fields = ("created_at", "updated_at")


# ----------------------------
# Provider
# ----------------------------

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "created_at")
    search_fields = ("name", "phone")
    readonly_fields = ("created_at", "updated_at")


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    pass


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





# -----------------------------
# Inline برای added_products و removed_products
# -----------------------------
class AddedProductInline(admin.TabularInline):
    model = AddedProduct
    extra = 1
    autocomplete_fields = ("product", "unit", "from_room", "provider", "taker")
    readonly_fields = ("quantity_in_kg",)
    fields = (
        "product",
        "quantity",
        "unit",
        "quantity_in_kg",
        "to_room",
        "from_room",
        "provider",
        "taker",
        "notes",
    )


class RemovedProductInline(admin.TabularInline):
    model = RemovedProduct
    extra = 1
    autocomplete_fields = ("product", "unit", "to_room", "provider", "taker")
    readonly_fields = ("quantity_in_kg",)
    fields = (
        "product",
        "quantity",
        "unit",
        "quantity_in_kg",
        "to_room",
        "from_room",
        "provider",
        "taker",
        "notes",
    )


# -----------------------------
# Admin Transaction
# -----------------------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    save_on_top = True

    list_display = (
        "id",
        "transaction_type",
        "date",
        "picking_period",
        "created_at",
    )

    list_filter = (
        "picking_period",
        "date",
    )

    search_fields = (
        "notes",
    )

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Core", {
            "fields": ("transaction_type", "notes")
        }),
        ("Period", {
            "fields": ("picking_period","date")
        }),
        ("System", {
            "fields": ("created_at", "updated_at")
        }),
    )

    autocomplete_fields = (
        "picking_period",
    )

    list_select_related = (
        "picking_period",
    )

    ordering = ("-date", "-created_at")

    inlines = [
        AddedProductInline,
        RemovedProductInline,
    ]


# -----------------------------
# Admin AddedProduct و RemovedProduct جداگانه (برای دسترسی مستقیم)
# -----------------------------
@admin.register(AddedProduct)
class AddedProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "transaction",
        "product",
        "quantity",
        "unit",
        "quantity_in_kg",
        "from_room",
        "to_room",
        "provider",
        "taker",
        "created_at",
    )
    search_fields = ("product__name", "transaction__room__name", "from_room__name")
    list_filter = ("unit", "from_room", "provider", "taker")


@admin.register(RemovedProduct)
class RemovedProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "transaction",
        "product",
        "quantity",
        "unit",
        "quantity_in_kg",
        "from_room",
        "to_room",
        "provider",
        "taker",
        "created_at",
    )
    search_fields = ("product__name", "transaction__room__name", "to_room__name")
    list_filter = ("unit", "to_room", "provider", "taker")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_room")
    list_select_related = ("user", "user_room")

    

    list_filter = ("user_room",)

    autocomplete_fields = ("user", "user_room")

    ordering = ("user",)
