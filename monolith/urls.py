from django.urls import path, include
from .views import ProductList, BucketAddView, BucketView, BookStoreView
app_name = 'monolith'
urlpatterns = [
    path('product/', include([
        path('list/', ProductList.as_view(), name='product_list'),

    ])),
    path('bucket/', include([
        path('create/', BucketAddView.as_view(), name='bucket_add'),
        path('prodcut_list/<int:user_id>/', BucketView.as_view(), name='bucket_detail'),
    ])),
    path('book_store', BookStoreView.as_view(), name='book_store_view'),
]
