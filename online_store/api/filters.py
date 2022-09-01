from django_filters import rest_framework as filters

from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

from .models import Order


class StatsFilter(filters.FilterSet):
    METRIC_MAP = {   # Defines the annotation Function in the get_metric() method, based on the metric that was passed.
        'price': Sum('products__price'),
        'count': Count('products'),
    }

    value_choices = (('price', 'price'), ('count', 'count'))

    date_start = filters.DateFilter(field_name='date',
                                    lookup_expr='gte',
                                    label='date_start',
                                    required=True)

    date_end = filters.DateFilter(field_name='date',
                                  lookup_expr='lte',
                                  label='date_end',
                                  required=True)

    metric = filters.ChoiceFilter(choices=value_choices,
                                  method='get_metric',
                                  empty_label=None,
                                  null_label=None,
                                  label='metric',
                                  required=True)

    class Meta:
        model = Order
        fields = ['date_start', 'date_end', 'metric']

    def get_metric(self, queryset, value, *args, **kwargs):
        if value is not None:
            metric = args[0]
            # Groups orders by month and applies Sum or Count based on the metric
            queryset = queryset.annotate(month=TruncMonth('date')).values('month') \
                .annotate(value=self.METRIC_MAP[metric]).values('month', 'value')
        return queryset
