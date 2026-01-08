from rest_framework import serializers
from .models import (
    Currency,
    PickingPeriod,
    ProductType,
    Product,
    Provider,
    Room,
    Taker,
    Transaction,
    Unit,
    AddedProduct,
    RemovedProduct,
    TransactionType,
)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"

class TakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taker
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = "__all__"

class PickingPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickingPeriod
        fields = "__all__"


class AddedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    unit = UnitSerializer(read_only=True)
    unit_id = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        source="unit",
        write_only=True
    )
    quantity_in_kg = serializers.DecimalField(
        max_digits=12,
        decimal_places=3,
        read_only=True
    )

    class Meta:
        model = AddedProduct
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
            "unit",
            "unit_id",
            "quantity_in_kg",
            "from_room",
            "provider",
            "taker",
            "notes",
        ]


class RemovedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    unit = UnitSerializer(read_only=True)
    unit_id = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        source="unit",
        write_only=True
    )
    quantity_in_kg = serializers.DecimalField(
        max_digits=12,
        decimal_places=3,
        read_only=True
    )

    class Meta:
        model = RemovedProduct
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
            "unit",
            "unit_id",
            "quantity_in_kg",
            "to_room",
            "provider",
            "taker",
            "notes",
        ]


class TransactionSerializer(serializers.ModelSerializer):
    added_products = AddedProductSerializer(many=True)
    removed_products = RemovedProductSerializer(many=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "date",
            "notes",
            "picking_period",
            "added_products",
            "removed_products",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        added_data = validated_data.pop("added_products", [])
        removed_data = validated_data.pop("removed_products", [])

        transaction = Transaction.objects.create(**validated_data)

        for item in added_data:
            AddedProduct.objects.create(transaction=transaction, **item)

        for item in removed_data:
            RemovedProduct.objects.create(transaction=transaction, **item)

        return transaction

    def update(self, instance, validated_data):
        added_data = validated_data.pop("added_products", [])
        removed_data = validated_data.pop("removed_products", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # حذف و بازساخت محصولات
        instance.added_products.all().delete()
        instance.removed_products.all().delete()

        for item in added_data:
            AddedProduct.objects.create(transaction=instance, **item)

        for item in removed_data:
            RemovedProduct.objects.create(transaction=instance, **item)

        return instance
