from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=1_000, decimal_places=2)

    def __str__(self):
        return self.title


class Order(models.Model):
    date = models.DateField()
    products = models.ManyToManyField(Product, blank=True, related_name='orders')
