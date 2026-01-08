from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TakerViewSet, ProviderViewSet, TransactionListCreateView, TransactionUpdateDeleteView, inventory_report

router = DefaultRouter()
router.register(r"takers", TakerViewSet)
router.register(r"providers", ProviderViewSet)


urlpatterns = [
    *router.urls,
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionUpdateDeleteView.as_view(), name='transaction-update-delete'),

    # new report
    path('report/inventory/', inventory_report, name='inventory_report'),

]
