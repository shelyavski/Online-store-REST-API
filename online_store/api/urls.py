from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'stats', views.StatsViewSet, basename='stats')

urlpatterns = [
    path('', include(router.urls)),
]
