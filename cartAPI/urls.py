from .views import CartViewSet
from rest_framework.routers import DefaultRouter

app_name = 'cartAPI'

router = DefaultRouter()

router.register(r'', CartViewSet, basename='cart')

urlpatterns = router.urls