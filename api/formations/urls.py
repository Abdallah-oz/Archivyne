from rest_framework.routers import DefaultRouter
from .views import FormationsView

router = DefaultRouter()
router.register('formations', FormationsView, basename='formations')

urlpatterns = router.urls

