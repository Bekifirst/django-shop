from django.urls import path
from myshop.views import add_to_cart, ajax_add_review, cart_view, index, product_detail_view, product_list_view, category_list_view, category_product_list_view, search_view, tag_list, vendor_detail_view, vendor_list_view

app_name = "myshop"

urlpatterns = [
    # Home page
    path('', index, name='index'),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),

    # Category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    # Vendor
    path("vendors/", vendor_list_view, name="vendor-list"),
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail"),

    # Tags
    path("product/tag/<slug:tag_slug>/", tag_list, name="tags"),

    # Add Review
    path("ajax_add_review/<int:pid>/", ajax_add_review , name="ajax_add_review"),

    # Search
    path("search/", search_view, name="search"),

    # add to cart
    path("add-to-cart/", add_to_cart, name="add-to-cart" ),


    #Cart page 
    path("cart/", cart_view, name="cart")
]