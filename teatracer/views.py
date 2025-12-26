from rest_framework.viewsets import ModelViewSet
from .models import Provider, Taker
from .serializers import TakerSerializer, ProviderSerializer


class TakerViewSet(ModelViewSet):
    queryset = Taker.objects.all()
    serializer_class = TakerSerializer


class ProviderViewSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
