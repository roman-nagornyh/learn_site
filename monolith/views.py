from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView, DeleteView
from .models import *
from django.db.models import Sum, Count


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/list.html'
    queryset = Product.objects.all().select_related('product_type')
    paginate_by = 10


class BucketView(LoginRequiredMixin, ListView):
    model = Bucket
    template_name = 'bucket/product_list.html'
    queryset = Bucket.objects.all()

    def get_queryset(self):
        return Bucket.objects.filter(status=False, user_id=self.kwargs.get('user_id')) \
            .values('product__id', 'product__name') \
            .annotate(sum_product=Sum('product__price'), count_product=Count('product__id'))\


    def get(self, request, *args, **kwargs):
        result = super(BucketView, self).get(request, *args, **kwargs)
        queryset = self.get_queryset()
        result.context_data['total_price'] = queryset.aggregate(Sum('sum_product'))
        return result


class BucketAddView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        post = request.POST
        Bucket.objects.create(product_id=post.get('product'), user_id=post.get('client'))
        reverse_obj = reverse('monolith:bucket_detail', kwargs={'user_id': post.get('client')})
        return HttpResponseRedirect(redirect_to=reverse_obj)


class UserLogin(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('monolith:product_list')
    redirect_authenticated_user = True


class DeleteBucketProductFirst(LoginRequiredMixin, DeleteView):
    model = Bucket

    def get_success_url(self):
        client_id = self.request.user.client.id
        return reverse('monolith:bucket_detail', kwargs={'user_id': client_id})

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


class BookStoreView(TemplateView):
    template_name = 'book_store.html'

    def get_context_data(self, **kwargs):
        results = []
        context = super(BookStoreView, self).get_context_data(**kwargs)
        context['publisher_results'] = results
        return context


# Разбор select_related
class TestView(TemplateView):
    template_name = 'test.html'

    def get(self, request, *args, **kwargs):
      
        return super(TestView, self).get(request, *args, **kwargs)


