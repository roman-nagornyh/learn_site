from django.db import models
from django.db.models import Sum, Count


class BucketManager(models.Manager):
    def product_sum(self):
        return self.values('product__id', 'product__name').annotate(sum_product=Sum('product__price'),
                                                                    count_product=Count('product__id'))
    # Разобраться

    def total_price(self):
        return self.aggregate(Sum('sum_product'))
