from rest_framework import serializers
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
    class Meta:
        model = Transaction
        fields = '__all__'
    read_only_fields = (
            'created_at',
            'updated_at',
            'total_cost',
        )
