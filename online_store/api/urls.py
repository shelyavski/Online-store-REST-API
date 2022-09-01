from django.urls import path, include
from . import views
from .routers import CustomApiRouter

router = CustomApiRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
