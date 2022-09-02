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
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                  many=True)

    class Meta:
        model = Order
        fields = ['id', 'date', 'products']

    def to_representation(self, instance):  # Presents the data in a 'nested serializer format'
        data = super().to_representation(instance)
        products = Product.objects.in_bulk(id_list=data['products'], field_name='id')
        formatted_products_list = []
        for product in products.values():
            formatted_products_list.append(
                {
                    'id': product.id,
                    'title': product.title,
                    'price': product.price
                }
            )
        data['products'] = formatted_products_list
        return data


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
