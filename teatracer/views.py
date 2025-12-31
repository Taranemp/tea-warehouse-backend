from rest_framework.viewsets import ModelViewSet
from .models import Provider, Taker, Transaction
from .serializers import TakerSerializer, ProviderSerializer, TransactionSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .services import calculate_transaction_total_cost



class TakerViewSet(ModelViewSet):
    queryset = Taker.objects.all()
    serializer_class = TakerSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer




class TransactionListCreateView(GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data) #convert transaction list to json
        serializer.is_valid(raise_exception=True)

        transaction = serializer.save()  
        calculate_transaction_total_cost(transaction) # total-cost calculation

        serializer = self.get_serializer(transaction)  # uodate data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TransactionUpdateDeleteView(GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def put(self, request, pk):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = serializer.save()  # update transaction in database
        calculate_transaction_total_cost(transaction) # recalculation 

        serializer = self.get_serializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
