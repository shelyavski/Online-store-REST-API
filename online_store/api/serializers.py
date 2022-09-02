from rest_framework import serializers

from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=1_000,
                                     decimal_places=2,
                                     coerce_to_string=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'date', 'products']

    def to_representation(self, instance):  # Presents the data in a 'nested serializer format'
        self.fields['products'] = ProductSerializer(many=True)
        return super(OrderSerializer, self).to_representation(instance)


class StatsSerializer(serializers.Serializer):
    month = serializers.DateField(read_only=True)
    value = serializers.DecimalField(max_digits=9999,
                                     decimal_places=2,
                                     coerce_to_string=False,
                                     read_only=True)

    class Meta:
        ref_name = None  # Hides the Serializer model from the swagger schema

    def to_representation(self, value):
        """Displays dates in the '2020 Jan' format instead of the standard '2020-01-01'
        and 'value' as an int instead of a float if metric = count"""

        representation = super(StatsSerializer, self).to_representation(value)

        # Date representation format
        representation['month'] = value['month'].strftime('%Y %b')

        # Metric representation format if metric=count
        if self.context['request'].query_params['metric'] == 'count':
            representation['value'] = int(value['value'])
        return representation
