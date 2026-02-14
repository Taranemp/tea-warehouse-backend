from django.db import models
from django.conf import settings

class Currency(models.Model):
    name = models.CharField(max_length=100)
    ratio = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=100)
    conversion_to_kg = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name="products"
    )
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=100, unique=True)
    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Taker(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="profile"
    )
    user_room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    def __str__(self):
        return self.user.username

class PickingPeriod(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Represents a transaction linked to a single room.
    Users can only access their own room's transactions.
    """

    transaction_type = models.ForeignKey("TransactionType", on_delete=models.PROTECT)

    date = models.DateField(db_index=True)
    notes = models.TextField(null=True, blank=True)
    picking_period = models.ForeignKey(
        "PickingPeriod",
        on_delete=models.PROTECT,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.date}"

    class Meta:
        verbose_name = "1. Transaction"
        verbose_name_plural = "1. Transactions"




class AddedProduct(models.Model):
    """
    Products added in a transaction.
    This includes metadata for later reporting.
    """
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="added_products"
    )
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.ForeignKey("Unit", on_delete=models.PROTECT)
    quantity_in_kg = models.DecimalField(max_digits=12, decimal_places=3, editable=False)

    # metadata
    to_room = models.ForeignKey("Room", on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    from_room = models.ForeignKey("Room", on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    provider = models.ForeignKey("Provider", on_delete=models.PROTECT, null=True, blank=True)
    taker = models.ForeignKey("Taker", on_delete=models.PROTECT, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.unit and self.quantity:
            self.quantity_in_kg = self.quantity * self.unit.conversion_to_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Added {self.quantity} {self.unit.name} of {self.product.name}"

    class Meta:
        verbose_name = "2. Added Product"
        verbose_name_plural = "2. Added Products"


class RemovedProduct(models.Model):
    """
    Products removed in a transaction.
    This includes metadata for later reporting.
    """
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="removed_products"
    )
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.ForeignKey("Unit", on_delete=models.PROTECT)
    quantity_in_kg = models.DecimalField(max_digits=12, decimal_places=3, editable=False)

    # metadata
    to_room = models.ForeignKey("Room", on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    from_room = models.ForeignKey("Room", on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    provider = models.ForeignKey("Provider", on_delete=models.PROTECT, null=True, blank=True)
    taker = models.ForeignKey("Taker", on_delete=models.PROTECT, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.unit and self.quantity:
            self.quantity_in_kg = self.quantity * self.unit.conversion_to_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Removed {self.quantity} {self.unit.name} of {self.product.name}"

    class Meta:
        verbose_name = "3. Removed Product"
        verbose_name_plural = "3. Removed Products"



