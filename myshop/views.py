from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from myshop.models import Product, Category, Vendor, CartOrder, CartOrderItems, wishlist, ProductImages, ProductReview, Address
from taggit.models import Tag
from django.db.models import Avg
from myshop.forms import ProductReviewForm
from django.template.loader import render_to_string

def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured= True)

    context = {
        "products": products
    }
    return render(request, 'myshop/index.html', context )


def product_list_view(request):
    products = Product.objects.filter(product_status="published", )

    context = {
        "products": products
    }
    return render(request, 'myshop/product-list.html', context )


def category_list_view(request):
    
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, 'myshop/category-list.html', context )



def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category= category)

    context = {
        "category": category,
        "products": products,
    }

    return render(request, "myshop/category-product-list.html", context)



def vendor_list_view(request):
    vendors = Vendor.objects.all()

    context = {
        "vendors": vendors
    }
    return render(request, "myshop/vendor-list.html", context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid = vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")

    context = {
        "vendor": vendor,
        "products": products
    }
    return render(request, "myshop/vendor-detail.html", context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid = pid)
    # product = get_object_or_404(Product, pid = pid)
    products = Product.objects.filter(category = product.category).exclude(pid=pid)

    # взять все отзывы смотря ток на продукты 
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # средняя оценка 
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))


    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    p_image = product.p_images.all()

    context = {
        "p": product,
        "make_review": make_review,
        "review_form": review_form,
        "p_image": p_image,
        "average_rating": average_rating,
        "reviews": reviews,
        "products": products,
    }

    return render(request, "myshop/product-detail.html", context)

def tag_list(request, tag_slug=None):
    products =Product.objects.filter(product_status="published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        products = products.filter(tags__in=[tag])          #искать по тагу который совпадает из моделей

    context = {
        "products": products,
        "tag": tag
    }

    return render(request, "myshop/tag.html", context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk = pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        "user": user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'average_reviews': average_reviews
        }
    )


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains = query, description__icontains = query).order_by("-date")

    context = {
        "products": products,
        "query": query,
    }

    return render(request, "myshop/search.html", context)


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],

    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amout = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amout += int(item['qty']) * float(item['price'])
        
        return render(request, "myshop/cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amout': cart_total_amout} )

    else:
        messages.warning(request, "Your cart is empty")
        return redirect("myshop:index")
