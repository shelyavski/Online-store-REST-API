from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import dateparse

from .serializers import ProductSerializer, OrderSerializer, StatsSerializer
from .models import Product, Order

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('products')
    serializer_class = OrderSerializer


class StatsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # Returns a report with the monthly sales distribution for the selected period between date_start and date_end.
    # If metric == “price”, then the value field contains the total sum of all sold products in this month.
    # If metric == “count”, then the value field contains the total count of all sold products in this month.

    serializer_class = StatsSerializer
    queryset = Order.objects.all()

    # Defines the annotation Function in list() method, based on the metric that was passed.
    METRIC_MAP = {
        'price': Sum('products__price'),
        'count': Count('products'),
    }

    @staticmethod
    def dates_are_valid(date_start, date_end):
        # Checks if dates are in the correct format
        try:
            date_start = dateparse.parse_date(date_start)
            date_end = dateparse.parse_date(date_end)

        except TypeError:
            return False

        # Checks that dates are not None or empty
        if date_start in (None, '') or date_end in (None, ''):
            return False

        # Checks if start date is after end date
        if date_start > date_end:
            return False

        return True

    # Decorator for swagger documentation
    @method_decorator(name='get', decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'date_start', openapi.IN_QUERY,
                description='Beginning of daterange.',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'date_end', openapi.IN_QUERY,
                description='End of daterange.',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'metric', openapi.IN_QUERY,
                description='Either displays number of items sold per month or the revenue per month',
                type=openapi.TYPE_STRING,
                enum=[metric for metric in METRIC_MAP],
                required=True
            ),
        ]
    ))
    def list(self, request, *args, **kwargs):
        # Validates the metric
        metric = self.request.query_params.get('metric', None)
        if metric not in self.METRIC_MAP.keys():
            error_msg = f"Query parameter 'metric' must be one of the following: {[key for key in self.METRIC_MAP.keys()]}"
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        # Validates date_start and date_end
        date_start = self.request.query_params.get("date_start", None)
        date_end = self.request.query_params.get("date_end", None)
        if not self.dates_are_valid(date_start, date_end):
            return Response('Please input valid date_start and date_end', status=status.HTTP_400_BAD_REQUEST)

        # Filter queryset by daterange --> group orders by month --> perform Sum or Count on each group
        filtered_queryset = Order.objects.filter(date__gte=date_start, date__lte=date_end).prefetch_related('products')
        queryset = filtered_queryset \
            .annotate(month=TruncMonth('date')).values('month') \
            .annotate(value=self.METRIC_MAP[metric]).values('month', 'value')

        # Paginating the result
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

