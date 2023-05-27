import orders.models

import products.models
from django.contrib.auth.models import User

from django.db.models import Sum, Count, Max, DecimalField

from django.db.models import DateTimeField, ExpressionWrapper, F


class DbConnectivity:
    temp = None

    @staticmethod
    def get_all_orders(self):
        return orders.models.Order.objects.all()

    @staticmethod
    def get_first_order(self):
        return orders.models.Order.objects.first()

    @staticmethod
    def get_all_products(self):
        return products.models.Product.objects.all()

    @staticmethod
    def get_registered_clients(self):
        temp = User.objects.filter(is_staff=False) # select
        temp2 = temp.values_list("id", "username", "email")
        return temp2

    @staticmethod
    def get_all_active_products(self):
        return products.models.Product.objects.filter(is_active=True)

    @staticmethod
    def get_new_orders(self):
        temp = orders.models.Order.objects.filter(status_id=1)
        return temp

    @classmethod
    def get_popular_product(cls):
        completed = cls.get_completed_orders()
        completed = completed.values_list('id', flat=True)
        completed = list(completed)
        res = orders.models.ProductInOrder.objects.values('product').filter(order__in=completed).annotate(dcount=Sum('nmb')).order_by()
        max_cnt = res.aggregate(max_cnt=Max('dcount'))
        res2 = res.filter(dcount=max_cnt['max_cnt'])
        return res2


    @classmethod
    def get_completed_orders(cls):
        res = orders.models.Order.objects.values().filter(status=3, complete=True)
        return res

    @classmethod
    def get_popular_product_cleaned(cls):
        res = cls.get_popular_product()
        res2 = res.values_list('product', flat=True)
        res3 = list(res2)
        res4 = products.models.Product.objects.filter(id__in=res3).values_list()
        return res4

    @classmethod
    def get_order_popularity(cls): # только по выполненным
        completed = cls.get_completed_orders()
        completed = completed.values_list('id', flat=True)
        completed = list(completed)
        res = orders.models.ProductInOrder.objects.values('product').filter(order__in=completed).annotate(
            dcount=Sum('nmb')).order_by()
        res = res.order_by('-dcount')
        #print(res)
        return res

    @classmethod
    def get_total_price_all(cls):
        completed = cls.get_completed_orders()
        completed = completed.values_list('id', flat=True)
        completed = list(completed)
        res = orders.models.ProductInOrder.objects.values('product', 'price_per_item').filter(order__in=completed).annotate(
            dcount=Sum('nmb')).order_by()
        res2 = res.annotate(total=ExpressionWrapper(F('dcount') * F('price_per_item'), output_field=DecimalField()))
        res3 = res2.order_by('-total')
        return res3

