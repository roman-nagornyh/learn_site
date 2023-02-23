from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView
from .models import *


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/list.html'
    queryset = Product.objects.all()
    paginate_by = 10


class BucketView(LoginRequiredMixin, ListView):
    model = Bucket
    template_name = 'bucket/product_list.html'
    queryset = Bucket.objects.all()

    def get_queryset(self):
        return Bucket.objects.filter(status=False, user_id=self.kwargs.get('user_id'))

    def get(self, request, *args, **kwargs):
        from django.db.models import Sum, Count
        queryset = self.get_queryset()
        total_buckets = queryset.values('product__id', 'product__name').annotate(sum_product=Sum('product__price'),
                                                                                 count_product=Count('product__id'))
        get_result = super(BucketView, self).get(request, *args, **kwargs)
        get_result.context_data['total_buckets'] = total_buckets
        return get_result


class BucketAddView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        post = request.POST
        bucket = Bucket.objects.create(product_id=post.get('product'), user_id=post.get('client'))
        reverse_obj = reverse('monolith:bucket_detail', kwargs={'pk': post.get('client')})
        return HttpResponseRedirect(redirect_to=reverse_obj)


class UserLogin(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('monolith:product_list')
    redirect_authenticated_user = True


class BookStoreView(TemplateView):
    template_name = 'book_store.html'

    def get_context_data(self, **kwargs):
        from django.db.models import Count
        results = Publisher.objects.annotate(count_books=Count('book'))
        context = super(BookStoreView, self).get_context_data(**kwargs)
        context['publisher_results'] = results
        return context
