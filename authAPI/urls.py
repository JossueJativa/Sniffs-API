from .views import UserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'authAPI'

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = router.urls