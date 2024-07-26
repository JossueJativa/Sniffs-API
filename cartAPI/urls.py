from .views import CartViewSet
from .consumers import CartConsumer
from rest_framework.routers import DefaultRouter

app_name = 'cartAPI'

router = DefaultRouter()

router.register(r'', CartViewSet, basename='cart')

urlpatterns = router.urls