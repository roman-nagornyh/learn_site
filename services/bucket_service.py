from django.contrib.auth.models import User
from application.models import Bucket
from django.db.models import Sum


class BucketService:
    def __init__(self, user: User):
        self.user = user

    def get_products(self):
        obj_list = Bucket.objects.product_sum().filter(
            status=False, client=self.user.client.pk
        )
        product_sum = obj_list.aggregate(Sum("sum_product"))
        return obj_list, product_sum

    def add(self, product_id: int) -> bool:
        res = Bucket.objects.create(
            product_id=product_id, client_id=self.user.client.pk
        )
        return res.pk is not None

    def delete(self, product_id: int) -> None:
        res = (
            Bucket.objects.filter(product_id=product_id, client_id=self.user.client.pk)
            .first()
            .delete()
        )

    def clean(self):
        Bucket.objects.filter(client_id=self.user.pk).delete()


class BucketSessionService:
    def __init__(self, session):
        pass
