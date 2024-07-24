from .views import ContractViewSet
from rest_framework.routers import DefaultRouter

app_name = 'contractAPI'

router = DefaultRouter()

router.register(r'', ContractViewSet, basename='contract')

urlpatterns = router.urls