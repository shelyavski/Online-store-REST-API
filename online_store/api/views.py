from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import ProductSerializer, OrderSerializer, StatsSerializer
from .models import Product, Order
from .filters import StatsFilter

from django_filters import rest_framework as filters


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('products')
    filter_backends = (filters.DjangoFilterBackend,)

    @property
    def filterset_class(self):
        if self.action == 'stats':
            return StatsFilter

    def get_serializer_class(self):
        if self.action == 'stats':
            return StatsSerializer
        return OrderSerializer

    """Provides a statistic for the monthly revenue or the number of items
    sold per month in a given daterange."""
    @action(
        methods=['get'],
        detail=False,
        url_path='stats',
        url_name='stats'
    )
    def stats(self, request):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)  # Applies StatsFilter to the queryset.

        # Paginating the result
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
