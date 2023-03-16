from django.urls import path, include
from .views import (
    ProductList,
    BucketAddView,
    BucketView,
    BookStoreView,
    DeleteBucketProductFirst,
    DeleteBucketProductAll,
    OrderCreateView,
    OrderListView
)
app_name = 'monolith'
urlpatterns = [
    path('product/', include([
        path('list/', ProductList.as_view(), name='product_list'),
    ])),
    path('bucket/', include([
        path('create/', BucketAddView.as_view(), name='bucket_add'),
        path('prodcut_list/<int:user_id>/', BucketView.as_view(), name='bucket_detail'),
        path('delete_product/<int:pk>', DeleteBucketProductFirst.as_view(), name='delete_product_first'),
        path('delete_product_all/<int:pk>', DeleteBucketProductAll.as_view(), name='delete_product_all'),
    ])),
    path('book_store', BookStoreView.as_view(), name='book_store_view'),
    path('order/', include([
        path('create/', OrderCreateView.as_view(), name='order_create'),
        path('list/', OrderListView.as_view(), name='order_list'),
    ]))
]
