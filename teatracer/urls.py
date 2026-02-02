from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CurrencyViewSet,
    TakerViewSet,
    ProviderViewSet,
    RoomViewSet,
    ProductViewSet,
    ProductTypeViewSet,
    UnitViewSet,
    PickingPeriodViewSet,
    TransactionTypeViewSet,

    TransactionListCreateView,
    TransactionUpdateDeleteView,
    inventory_report,



)

router = DefaultRouter()
router.register(r"currencies", CurrencyViewSet)
router.register(r"takers", TakerViewSet)
router.register(r"providers", ProviderViewSet)
router.register(r"rooms", RoomViewSet)
router.register(r"products", ProductViewSet)
router.register(r"product-types", ProductTypeViewSet)
router.register(r"unites", UnitViewSet)
router.register(r"picking-periods", PickingPeriodViewSet)
router.register(r"transaction-types", TransactionTypeViewSet)


urlpatterns = [
    *router.urls,
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionUpdateDeleteView.as_view(), name='transaction-update-delete'),

    # new report
    path('report/inventory/', inventory_report, name='inventory_report'),

]
