from .views import ProductViewSet
from rest_framework.routers import DefaultRouter

app_name = 'productsAPI'

router = DefaultRouter()

router.register(r'', ProductViewSet, basename='product')

urlpatterns = router.urls