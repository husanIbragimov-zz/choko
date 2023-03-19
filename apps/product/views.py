from datetime import datetime
from django.db.models import Q
from django.views import View
from apps.product.forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect

from apps.order.models import Variant
from apps.product.models import Category, Banner, Brand, Product, Rate, Advertisement, Color
from django.core.paginator import Paginator


def index(request):
    advertisements = Advertisement.objects.all().order_by('-id')
    product = Product.objects.filter(is_active=True).order_by('-id')
    category = Category.objects.filter(is_active=True)
    brand = Brand.objects.all().order_by('-id')
    banner = Banner.objects.all()
    last_3_products = product.order_by('-created_at')
    top_rated_products = sorted(product, key=lambda t: t.mid_rate, reverse=True)
    top_viewed_products = product.order_by('-view')
    query = []
    for qs in product:
        if qs.percentage > 20:
            query.append(qs)

    # filters
    cat = request.GET.get('cat')
    status = request.GET.get('status')
    search = request.GET.get('search')
    status_index = 'featured'
    if cat:
        product = product.filter(category__title__icontains=cat)
    if status:
        if status == "popular":
            product = sorted(product, key=lambda t: t.mid_rate, reverse=True)
            status_index = 'popular'
        elif status == "top_rated":
            product = product.order_by('-view')
            status_index = 'top_rated'
    if search:
        product = product.filter(Q(title__icontains=search) | Q(category__title__icontains=search))
    context = {
        'advertisements': advertisements[:1],
        'last_advertisements': advertisements[1:2],
        'discounts': query[2:3],
        'queryset': query[:2],

        'products': product[:12],
        'objects': product[12:24],
        'categories': category,
        'brands': brand,
        'banners': banner[:5],
        'last_products': last_3_products,
        'top_rate_products': top_rated_products,
        'top_viewed_products': top_viewed_products,
        'status_index': status_index
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'page-about.html', {})


def shop_list(request):
    products = Product.objects.filter(is_active=True).order_by('-id')
    category = Category.objects.filter(is_active=True)
    brands = Brand.objects.all().order_by('-id')
    top_rate_products = sorted(products, key=lambda t: t.mid_rate)
    last_3_products = products.order_by('-view')
    print(category)

    # filter
    cat = request.GET.get('cat')
    top_rated = request.GET.get('top_rated')
    search = request.GET.get('search')
    advertisement = request.GET.get('advertisement')
    brand = request.GET.get('brand')

    if cat:
        products = products.filter(category__title__icontains=cat)
    if search:
        products = products.filter(
            Q(title__icontains=search) | Q(status__contains=search) | Q(brand__title__icontains=search) | Q(
                description=search))
    if advertisement:
        products = products.filter(advertisement__title__contains=advertisement)
    if brand:
        products = products.filter(brand__title__icontains=brand)

    query = []
    for qs in products:
        if qs.percentage > 20:
            query.append(qs)

    # paginator
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'discounts': query,
        'page_obj': products,
        'cats': category,
        'brands': brands,
        'last_3_products': last_3_products[:3],
        'top_rate_products': top_rate_products
    }
    return render(request, 'shop.html', context)


def shop_details(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(~Q(id=product.id), category__in=[i.id for i in product.category.all()],
                                              is_active=True)

    new_products = Product.objects.filter(~Q(id=product.id), is_active=True).order_by('-created_at')[:5]
    comments = Rate.objects.filter(product_id=id).order_by('-id')
    category = Category.objects.filter(is_active=True)
    colors = Color.objects.all()
    if product.id:
        product.view += 1
        product.save()
    # comments
    comment = None
    if request.method == "POST":
        form = CommentForm(data=request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect(f'/shop-details/{product.id}#comments')

    else:
        form = CommentForm()

    variants = Variant.objects.all()
    context = {
        'form': form,
        "colors": colors,
        "product": product,
        "variants": variants,
        'comments': comments,
        "new_products": new_products,
        "categories": category,
        "related_products": related_products[:4],
    }
    return render(request, "shop-details.html", context)
