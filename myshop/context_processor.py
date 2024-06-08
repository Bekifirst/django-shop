from myshop.models import Product, Category, Vendor, CartOrder, CartOrderItems, wishlist, ProductImages, ProductReview, Address

def default(request):
    categories = Category.objects.all()
    # address = Address.objects.get(user=request.user.id)

    return {
        'categories': categories,
        'address': 'address',
    }