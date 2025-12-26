from rest_framework.routers import DefaultRouter
from .views import TakerViewSet, ProviderViewSet

router = DefaultRouter()
router.register(r"takers", TakerViewSet)
router.register(r"providers", ProviderViewSet)

urlpatterns = router.urls
