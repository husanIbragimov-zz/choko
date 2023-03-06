from datetime import datetime

from django.views import View
from django.shortcuts import render
from apps.product.models import Category, Banner, Brand, Tag, Product, Rate, Advertisement
from django.core.paginator import Paginator


class IndexView(View):

    def get(self, request):
        advertisements = Advertisement.objects.all().order_by('-id')
        product = Product.objects.filter(is_active=True).order_by('-id')
        category = Category.objects.filter(is_active=True)
        brand = Brand.objects.all().order_by('-id')
        banner = Banner.objects.all()
        last_3_products = product.order_by('-created_at')
        top_rate_products = product.order_by('-mid_rate')
        top_viewed_products = product.order_by('-view')
        query = []
        for qs in product:
            if qs.percentage > 20:
                query.append(qs)

        # filters
        cat = request.GET.get('cat')
        if cat:
            product = product.filter(category__title__icontains=cat)

        context = {
            'advertisements': advertisements[:1],
            'discounts': query[2:3],
            'queryset': query[:2],

            'products': product[:12],
            'objects': product[12:24],
            'categories': category,
            'brands': brand,
            'banners': banner[:5],
            'last_products': last_3_products,
            'top_rate_products': top_rate_products,
            'top_viewed_products': top_viewed_products
        }
        return render(request, 'index-3.html', context)


def about(request):
    return render(request, 'page-about.html', {})


def shop_list(request):
    products = Product.objects.all().order_by('-id')
    category = Category.objects.filter(is_active=True)
    brands = Brand.objects.all().order_by('-id')
    top_rate_products = products.order_by('-mid_rate')
    last_3_products = products.order_by('-view')

    # filter
    cat = request.GET.get('cat')
    top_rated = request.GET.get('top_rated')
    if cat:
        products = products.filter(category__title__icontains=cat)

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
        'categories': category,
        'brands': brands,
        'last_3_products': last_3_products[:3],
        'top_rate_products': top_rate_products
    }
    return render(request, 'shop-grid-left.html', context)
