import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import TemplateView, DeleteView
from .models import *
from django.db.models import Sum, Count


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/list.html'
    queryset = Product.objects.all().select_related('product_type')
    paginate_by = 20


class BucketView(LoginRequiredMixin, ListView):
    model = Bucket
    template_name = 'bucket/product_list.html'
    queryset = Bucket.objects.product_sum()

    def get_queryset(self):
        return self.queryset.filter(status=False, client_id=self.request.user.client.id)

    def get(self, request, *args, **kwargs):
        result = super(BucketView, self).get(request, *args, **kwargs)
        queryset = self.get_queryset()
        result.context_data['total_price'] = queryset.aggregate(Sum('sum_product'))
        return result


class BucketAddView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        post = request.POST
        Bucket.objects.create(product_id=post.get('product'),
                              client_id=request.user.client.id)
        return HttpResponseRedirect(redirect_to=reverse('monolith:bucket_detail'))


class UserLogin(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('monolith:product_list')
    redirect_authenticated_user = True


class DeleteBucketProductFirst(LoginRequiredMixin, DeleteView):
    model = Bucket

    def get_success_url(self):
        return reverse('monolith:bucket_detail')

    def get_queryset(self):
        return Bucket.objects.filter(product_id=self.kwargs.get('pk', False))
    
    def get_object(self, queryset=None):
        return self.get_queryset().first()


class DeleteBucketProductAll(DeleteBucketProductFirst):

    def delete(self, request, *args, **kwargs):
        deleted_products = self.queryset.all()
        for product in deleted_products:
            product.delete()
        return HttpResponseRedirect(self.success_url)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    queryset = Order.objects.prefetch_related('products_order', 'products_order__product')
    template_name = 'orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.queryset.filter(client_id=self.request.user.client.id)


class OrderCreateView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        from .models import Order, ProductOrder, OrderStatus
        post = request.POST
        identity_list = post.getlist('product_id', [])
        count_list = post.getlist('count_product', [])
        price_list = post.getlist('price', [])
        total_price = post.get('total_price', 0)
        order = Order.objects.create(
            order_date=datetime.datetime.now(),
            status=OrderStatus.objects.get(name='Оформлен'),
            client_id=request.user.client.id,
            total_price=total_price
        )
        created_list = []
        for index, pr_id in enumerate(identity_list):
            created_list.append(
                ProductOrder(order_id=order.id, product_id=pr_id,
                             count=count_list[index], price=price_list[index])
            )
        ProductOrder.objects.bulk_create(created_list)
        Bucket.objects.filter(product_id__in=identity_list).delete()
        return HttpResponseRedirect(reverse('monolith:order_list'))
