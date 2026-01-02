from rest_framework import serializers
from .models import (
    Currency,
    MovementType,
    PickingPeriod,
    ProductType,
    Product,
    Provider,
    Room,
    Taker,
    Transaction,
    Unit,
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


class PickingPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickingPeriod
        fields = "__all__"


class MovementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementType
        fields = "__all__"




class TransactionSerializer(serializers.ModelSerializer):
    total_cost = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = "__all__"

    def _calculate_total_cost(self, validated_data):
        unit_price = validated_data.get("unit_price")
        quantity = validated_data.get("quantity")

        if unit_price is None:
            return None

        return quantity * unit_price

    def create(self, validated_data):
        validated_data["total_cost"] = self._calculate_total_cost(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.unit_price = validated_data.get(
            "unit_price", instance.unit_price
        )
        instance.quantity = validated_data.get(
            "quantity", instance.quantity
        )

        if instance.unit_price is None:
            instance.total_cost = None
        else:
            instance.total_cost = instance.quantity * instance.unit_price

        return super().update(instance, validated_data)

