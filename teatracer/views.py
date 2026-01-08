from rest_framework.viewsets import ModelViewSet
from .models import (
    PickingPeriod,
    ProductType,
    Product,
    Provider,
    Room,
    Taker,
    Transaction,
    Unit,
    Currency,
    AddedProduct,
    RemovedProduct,
)
from .serializers import (
    PickingPeriodSerializer,
    ProductSerializer,
    ProductTypeSerializer,
    ProviderSerializer,
    RoomSerializer,
    TakerSerializer,
    UnitSerializer,
    CurrencySerializer,
    TransactionSerializer,
    AddedProductSerializer,
    RemovedProductSerializer,
)

from rest_framework.permissions import IsAdminUser
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework.decorators import api_view


# ----------------------------
# Standard ViewSets
# ----------------------------

class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class TakerViewSet(ModelViewSet):
    queryset = Taker.objects.all()
    serializer_class = TakerSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductTypeViewSet(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class UnitViewSet(ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class PickingPeriodViewSet(ModelViewSet):
    queryset = PickingPeriod.objects.all()
    serializer_class = PickingPeriodSerializer


# ----------------------------
# Transaction Views
# ----------------------------

class TransactionListCreateView(GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        return Response(
            self.get_serializer(transaction).data,
            status=status.HTTP_201_CREATED
        )


class TransactionUpdateDeleteView(GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        return Response(self.get_serializer(transaction).data)

    def delete(self, request, pk):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["GET"])
def inventory_report(request):
    result = {}

    rooms = Room.objects.all()
    products = Product.objects.all()

    for room in rooms:
        room_data = {}

        for product in products:
            added_qty = AddedProduct.objects.filter(
                product=product,
                to_room=room
            ).aggregate(total=Sum("quantity_in_kg"))["total"] or 0

            removed_qty = RemovedProduct.objects.filter(
                product=product,
                from_room=room
            ).aggregate(total=Sum("quantity_in_kg"))["total"] or 0

            current_qty = added_qty - removed_qty

            if current_qty != 0:
                room_data[product.name] = float(current_qty)

        result[room.name] = room_data

    return Response(result)