from .views import QuotationHeaderViewSet, QuotationDetailViewSet
from rest_framework.routers import DefaultRouter

app_name = 'quotation'

router = DefaultRouter()

router.register(r'header', QuotationHeaderViewSet, basename='quotation-header')
router.register(r'detail', QuotationDetailViewSet, basename='quotation-detail')

urlpatterns = router.urls