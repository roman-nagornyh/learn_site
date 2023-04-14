import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import TemplateView, DeleteView, CreateView
from .models import *
from django.db.models import Sum, Count
from django_filters.views import FilterView
from .filters import ProductFilter


class ProductList(LoginRequiredMixin, FilterView):
    model = Product
    template_name = 'product/list.html'
    queryset = Product.objects.all().select_related('product_type')
    filterset_class = ProductFilter
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data()
        get_data = self.request.GET
        brand_id = get_data.get('brand_id', False)
        product_type_id = get_data.get('product_type_id', False)
        context_extra = {
            'brands': Brand.objects.all(),
            'product_types': TypeProduct.objects.all(),
            'brand_id': int(brand_id) if brand_id else '',
            'name': get_data.get('name', ''),
            'product_type_id': int(product_type_id) if product_type_id else ''
        }
        return context | context_extra


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
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.queryset.filter(client_id=self.request.user.client.id)


class OrderCreateViewNew(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'orders/create.html'
    fields = '__all__'


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




