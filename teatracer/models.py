from django.db import models


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
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Taker(models.Model):
    name = models.CharField(max_length=150)
    note = models.TextField(null=True, blank=True)
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


class PickingPeriod(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MovementType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Transaction model representing movements of products between rooms, providers, and takers.

    Tracks product quantities, pricing, and related metadata for inventory management.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="transactions"
    )
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    quantity_in_kg = models.DecimalField(max_digits=12, decimal_places=3)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name="transactions"
    )
    date = models.DateField(db_index=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Room relationships (for internal movements)
    to_room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="transactions_to",
        null=True,
        blank=True
    )
    from_room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="transactions_from",
        null=True,
        blank=True
    )
    
    # External relationships
    from_provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT,
        related_name="transactions",
        null=True,
        blank=True
    )
    to_taker = models.ForeignKey(
        Taker,
        on_delete=models.PROTECT,
        related_name="transactions",
        null=True,
        blank=True
    )
    
    # Optional relationships
    picking_period = models.ForeignKey(
        PickingPeriod,
        on_delete=models.PROTECT,
        related_name="transactions",
        null=True,
        blank=True
    )
    movement_type = models.ForeignKey(
        MovementType,
        on_delete=models.PROTECT,
        related_name="transactions"
    )
    
    # Pricing fields
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        null=True,
        blank=True
    )
    total_cost = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        null=True,
        blank=True
    )
    currency = models.CharField(max_length=10)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['product', 'date']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.unit.name} on {self.date}"