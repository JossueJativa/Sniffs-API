from .views import BillHeaderViewSet, BillDetailViewSet
from rest_framework.routers import DefaultRouter

app_name = 'billAPI'

router = DefaultRouter()

router.register(r'header', BillHeaderViewSet, basename='bill-header')
router.register(r'detail', BillDetailViewSet, basename='bill-detail')

urlpatterns = router.urls