from rest_framework.viewsets import ModelViewSet
from .models import (
    MovementType,
    PickingPeriod,
    ProductType,
    Product,
    Provider,
    Room,
    Taker,
    Transaction,
    Unit,
    Currency
)

from .serializers import (
    MovementTypeSerializer,
    PickingPeriodSerializer,
    ProductTypeSerializer,
    ProviderSerializer,
    RoomSerializer,
    TakerSerializer,
    UnitSerializer,
    CurrencySerializer,
    TransactionSerializer,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from rest_framework.decorators import api_view


class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer



class TakerViewSet(ModelViewSet):
    queryset = Taker.objects.all()
    serializer_class = TakerSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer



class TransactionListCreateView(GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]


    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        transaction = serializer.save()  # recalculation inside serializer
        return Response(
            self.get_serializer(transaction).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
def inventory_report(request):
    result = {}

    rooms = Room.objects.all()
    products = Product.objects.all()

    for room in rooms:
        room_data = {}
        for product in products:
            # total income
            total_in = Transaction.objects.filter(
                to_room=room,
                product=product
            ).aggregate(total=Sum('quantity'))['total'] or 0

            # total outcome
            total_out = Transaction.objects.filter(
                from_room=room,
                product=product
            ).aggregate(total=Sum('quantity'))['total'] or 0

            current_qty = total_in - total_out

            if current_qty > 0:
                room_data[product.name] = float(current_qty)

        result[room.name] = room_data

    return Response(result)
