from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist

from .models import Product, Order

# TODO: ADD swagger to api root


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=1_000, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False, read_only=False)

    class Meta:
        model = Order
        fields = ['id', 'date', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        products = []

        # Check if a product with this title already exists in the DB
        for product_data in products_data:

            # If it exists update product price.
            try:
                product = Product.objects.get(title=product_data['title'])
                product.price = product_data['price']

            # If not create a new product.
            except ObjectDoesNotExist:
                product = Product.objects.create(**product_data)
            products.append(product)

        order = Order.objects.create(**validated_data)
        order.products.set(products)
        return order

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products')
        products = instance.products.all()
        products = list(products)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        # For many products
        for product_data in products_data:
            product = products.pop(0)
            product.title = product_data.get('title', product.title)
            product.price = product_data.get('price', product.price)
            product.save()

        return instance


class StatsSerializer(serializers.Serializer):
    month = serializers.DateField(read_only=True)
    value = serializers.DecimalField(max_digits=9999, decimal_places=2, coerce_to_string=False,
                                     read_only=True)

    class Meta:
        ref_name = None  # Hides the Serializer model from the swagger schema

    def to_representation(self, value):
        """Displays dates in the '2020 Jan' format instead of the standard '2020-01-01'
        and 'value' as an int instead of a float if metric = count"""

        representation = super(StatsSerializer, self).to_representation(value)

        # Date representation
        representation['month'] = value['month'].strftime('%Y %b')

        # Representation if metric=count
        if self.context['request'].query_params['metric'] == 'count':
            representation['value'] = int(value['value'])
        return representation
