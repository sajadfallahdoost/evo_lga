from django.urls import path
from product.api.views import (
    product_list, product_detail,
    fetch_products_from_external_api,
    external_product_list,
    add_product_review,
    list_product_reviews,
    list_related_products,
    add_related_product,
    filtered_product_list,
    brand,
    in_stock_product_list
)


urlpatterns = [
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    path('products/external/', external_product_list, name='external-product-list'),
    path('products/fetch-external/', fetch_products_from_external_api, name='fetch-products-external'),
    path('brand/', brand, name='brand'),
    path('in_stock_product_list/', in_stock_product_list, name='in_stock_product_list'),
    path('products/filtered/', filtered_product_list, name='filtered-product-list'),
    path("products/<int:product_id>/related/add/", add_related_product, name="add_related_product"),
    path("products/<int:product_id>/related/", list_related_products, name="list_related_products"),
    path("products/<int:product_id>/reviews/add/", add_product_review, name="add_product_review"),
    path("products/<int:product_id>/reviews/", list_product_reviews, name="list_product_reviews"),
]
