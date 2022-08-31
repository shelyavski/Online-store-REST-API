from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)  # TODO: Fix stats endpoint   ---> api/stats

urlpatterns = [
    path('', include(router.urls)),
]
