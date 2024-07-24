from .views import CommentViewSet
from rest_framework.routers import DefaultRouter

app_name = 'commentAPI'

router = DefaultRouter()

router.register(r'', CommentViewSet, basename='comment')

urlpatterns = router.urls