from django.utils import timezone
from django.db.models import Q, Min
from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView

from api.product.serializers import VariantSerializer
from apps.base.models import Variant
from apps.product.api.serializers import AppProductSerializer, ProductRetrieveSerializer
from apps.product.forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from apps.product.models import Category, Banner, Brand, Product, Rate, Advertisement, Color, ProductImage, \
    Currency, BannerDiscount, Author, Size
from django.core.paginator import Paginator
from rest_framework.response import Response


def range_filter(high, low, products):
    currency = Currency.objects.last().amount
    active_variant = Variant.objects.last().percent

    products = products.filter(
        uzs_price__gte=low, uzs_price__lte=high)

    return products


def index(request):
    advertisements = Advertisement.objects.all().order_by('-id')
    product = Product.objects.filter(is_active=True).order_by('?')
    category = Category.objects.filter(is_active=True)
    brand = Brand.objects.all().order_by('-id')
    banner = Banner.objects.all()
    last_3_products = product.order_by('-created_at')
    top_rated_products = sorted(product, key=lambda t: t.mid_rate, reverse=True)
    top_viewed_products = product.order_by('-view')
    banner_discounts = BannerDiscount.objects.filter(product__isnull=False, is_active=True)

    # Generate the query list using list comprehension.
    query = [qs for qs in product if qs.percentage >= 20]

    # filters
    cat = request.GET.get('cat')
    status = request.GET.get('status')
    search = request.GET.get('search')
    status_index = 'featured'
    if cat:
        product = product.filter(category__title__icontains=cat)
    if status:
        if status == "clothing":
            product = product.filter(product_type='clothing')
            status_index = 'clothing'
        elif status == "books":
            product = product.filter(product_type='books')
            status_index = 'books'
        elif status == "product":
            product = product.filter(product_type='product')
            status_index = 'product'
    if search:
        product = product.filter(Q(title__icontains=search) | Q(category__title__icontains=search))

    for banner_discount in banner_discounts:
        now = timezone.now()
        deadline = banner_discount.deadline
        if now >= deadline:
            banner_discount.is_active = False
            banner_discount.save()

    context = {
        'advertisements': advertisements[:1],
        'last_advertisements': advertisements[1:2],
        'discounts': query[2:3],
        'queryset': query[:2],

        'products': product[:20],
        'objects': product[21:41],
        'second_objects': product[42:62],
        'categories': category,
        'brands': brand,
        'banners': banner[:5],
        'last_products': last_3_products,
        'top_rate_products': top_rated_products,
        'top_viewed_products': top_viewed_products,
        'status_index': status_index,
        'banner_discounts': banner_discounts[:1],
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'page-about.html', {})


def shop_list(request):
    products = Product.objects.filter(is_active=True).order_by('?')
    category = Category.objects.filter(is_active=True)
    brands = Brand.objects.all().order_by('-id')
    top_rate_products = sorted(products, key=lambda t: t.mid_rate)
    last_3_products = products.order_by('-view')

    # filter
    cat = request.GET.get('cat')
    search = request.GET.get('search')
    advertisement = request.GET.get('advertisement')
    brand = request.GET.get('brand')
    active_cat = False
    active_cat_name = None
    active_brand = False
    active_brand_name = None
    if cat:
        active_cat = True
        active_cat_name = cat
        products = products.filter(category__title__icontains=cat)
    if search:
        products = products.filter(
            Q(title__icontains=search) | Q(status__contains=search) | Q(brand__title__icontains=search) | Q(
                description=search))
    if advertisement:
        products = products.filter(advertisement__title__contains=advertisement)
    if brand:
        active_brand = True
        active_brand_name = brand
        products = products.filter(brand__title__icontains=brand)

    # paginator
    page_number = request.GET.get('page')
    paginator = Paginator(products, 20)
    paginated_products = paginator.get_page(page_number)

    # Generate the query list using list comprehension.
    query = [qs for qs in products if qs.percentage >= 20]

    context = {
        'products': paginated_products,
        'discounts': query,
        'page_obj': paginated_products,
        'cats': category,
        'active_cat': active_cat,
        'active_cat_name': active_cat_name,
        'active_brand': active_brand,
        'active_brand_name': active_brand_name,
        'brands': brands,
        'last_3_products': last_3_products[:3],
        'top_rate_products': top_rate_products
    }
    return render(request, 'shop.html', context)


def shop_appliances(request):
    products = Product.objects.filter(is_active=True, product_type='product').order_by('?')
    category = Category.objects.filter(is_active=True, product_type='product')
    brands = Brand.objects.filter(product_type='product').order_by('-id')
    top_rate_products = sorted(products, key=lambda t: t.mid_rate)
    last_3_products = products.order_by('-view')

    # filter
    selected_range = request.GET.get('selected_range', '')
    min_value = request.GET.get('min-value', 0)
    max_value = request.GET.get('max-value', 0)
    cat = request.GET.get('cat', '')
    search = request.GET.get('search', '')
    brand = request.GET.get('brand', '')
    # paginator
    page_number = request.GET.get('page', '')

    active_cat_name = cat
    active_brand_name = brand
    active_page = page_number
    search_name = search
    high = max_value
    low = min_value

    if float(max_value) > 0 or float(min_value) > 0:
        # range filter
        products = range_filter(high, low, products)

    if cat or brand:
        products = products.filter(
            Q(category__title=active_cat_name) | Q(brand__title=active_brand_name)
        )

    if search_name:
        products = products.filter(
            Q(title__icontains=search_name) | Q(status__contains=search_name) | Q(
                brand__title__icontains=search_name) | Q(
                description=search_name))

    paginator = Paginator(products, 20)
    paginated_products = paginator.get_page(page_number)

    # Generate the query list using list comprehension.
    query = [qs for qs in products if qs.percentage >= 20]

    context = {
        'products': paginated_products,
        'discounts': query,
        'page_obj': paginated_products,
        'cats': category,
        'active_cat_name': active_cat_name,
        'search_name': search_name,
        'active_brand_name': active_brand_name,
        'active_page': active_page,
        'selected_range': selected_range,
        'high': high,
        'low': low,
        'brands': brands,
        'last_3_products': last_3_products[:3],
        'top_rate_products': top_rate_products
    }
    return render(request, 'shop-2.html', context)


def shop_books(request):
    products = Product.objects.filter(is_active=True, product_type='book').order_by('?')
    category = Category.objects.filter(is_active=True, product_type='book')
    brands = Brand.objects.filter(product_type='book').order_by('-id')
    authors = Author.objects.all().order_by('name')

    authors_data = list(map(int, request.POST.getlist('authors')))

    # filter
    cat = request.GET.get('cat', '')
    search = request.GET.get('search', '')
    lang = request.GET.get('lang', '')
    inscription = request.GET.get('inscription', '')
    wrapper = request.GET.get('wrapper', '')
    advertisement = request.GET.get('advertisement', '')
    brand = request.GET.get('brand', '')
    author_list = request.GET.get('author', '')
    # paginator
    page_number = request.GET.get('page', '')
    min_value = request.GET.get('min-value', 0)
    max_value = request.GET.get('max-value', 0)
    if min_value == '':
        min_value = 0
    if max_value == '':
        max_value = 0

    active_cat_name = cat
    active_brand_name = brand
    search_name = search
    lang_name = lang
    inscription_name = inscription
    wrapper_name = wrapper
    author_name = author_list
    active_page = page_number
    high = max_value
    low = min_value

    if float(max_value) > 0 or float(min_value) > 0:
        # range filter
        products = range_filter(high, low, products)

    if cat or brand or lang or inscription or author_list or len(authors_data) > 0:
        products = products.filter(
            Q(category__title=active_cat_name) | Q(brand__title=active_brand_name) |
            Q(language=lang_name) | Q(yozuv__exact=inscription_name) | Q(author__id__in=authors_data)
        )

    if inscription_name:
        products = products.filter(Q(yozuv=inscription_name))

    if wrapper_name:
        products = products.filter(Q(product_images__wrapper=wrapper_name))

    paginator = Paginator(products, 20)
    paginated_products = paginator.get_page(page_number)

    # Generate the query list using list comprehension.
    query = [qs for qs in products if qs.percentage >= 20]

    context = {
        'authors': authors,
        'products': paginated_products,
        'discounts': query,
        'page_obj': paginated_products,
        'authors_data': authors_data,
        'cats': category,
        'active_cat_name': active_cat_name,
        'active_brand_name': active_brand_name,
        'search_name': search_name,
        'lang_name': lang_name,
        'inscription_name': inscription_name,
        'wrapper_name': wrapper_name,
        'author_name': author_name,
        'active_page': active_page,
        'brands': brands,
        'high': high,
        'low': low

    }
    return render(request, 'shop-book.html', context)


def shop_clothes(request):
    products = Product.objects.filter(is_active=True, product_type='clothing').order_by('?')
    category = Category.objects.filter(is_active=True, product_type='clothing')
    brands = Brand.objects.filter(product_type='clothing').order_by('-id')
    top_rate_products = sorted(products, key=lambda t: t.mid_rate)
    last_3_products = products.order_by('-view')
    colors = Color.objects.all().order_by('title').distinct('title')
    sizes = Size.objects.all()

    colors_ids = list(map(int, request.POST.getlist('colors')))
    sizes_ids = list(map(int, request.POST.getlist('sizes')))

    page_number = request.GET.get('page', '')
    cat = request.GET.get('cat', '')
    search = request.GET.get('search', '')
    advertisement = request.GET.get('advertisement', '')
    brand = request.GET.get('brand', '')
    min_value = request.GET.get('min-value', 0)
    max_value = request.GET.get('max-value', 0)
    if min_value == '':
        min_value = 0
    if max_value == '':
        max_value = 0

    active_cat_name = cat
    active_brand_name = brand
    high = max_value
    low = min_value
    active_page = page_number

    if float(max_value) > 0 or float(min_value) > 0:
        # range filter
        products = range_filter(high, low, products)

    if cat or brand or len(colors_ids) > 0 or len(sizes_ids) > 0:
        products = products.filter(
            Q(category__title=active_cat_name) | Q(brand__title=active_brand_name) |
            Q(product_images__color__in=colors_ids) | Q(size__in=sizes_ids)
        )

    if search:
        products = products.filter(
            Q(title__icontains=search) | Q(status__contains=search) | Q(brand__title__icontains=search) | Q(
                description=search))
    if advertisement:
        products = products.filter(advertisement__title__contains=advertisement)

    # paginator
    paginator = Paginator(products.distinct(), 20)
    paginated_products = paginator.get_page(page_number)

    # Generate the query list using list comprehension.
    query = [qs for qs in products if qs.percentage >= 20]

    context = {
        'high': high,
        'low': low,
        'active_page': active_page,
        'sizes': sizes,
        'colors': colors,
        'colors_ids': colors_ids,
        'sizes_ids': sizes_ids,
        'products': paginated_products,
        'discounts': query,
        'page_obj': paginated_products,
        'cats': category,
        'active_cat_name': active_cat_name,
        'active_brand_name': active_brand_name,
        'brands': brands,
        'last_3_products': last_3_products[:3],
        'top_rate_products': top_rate_products
    }
    return render(request, 'shop-clothing.html', context)


def shop_details(request, pk):
    product = get_object_or_404(Product, id=pk)
    related_products = Product.objects.filter(~Q(id=product.id), category__in=[i.id for i in product.category.all()],
                                              is_active=True)
    images = ProductImage.objects.filter(product_id=pk)
    data = []
    data_ids = []
    for image in images:
        if product.product_type == 'book':
            if image.wrapper in data_ids:
                data.append({
                    "id": image.id,
                    'wrapper': image.wrapper
                })
                number = [d.get('count') for d in data if d['wrapper'] == image.wrapper]
                data[-1]['count'] = number[0] + 1
            else:
                data.append({
                    "id": image.id,
                    'count': 1,
                    'wrapper': image.wrapper
                })
                data_ids.append(image.wrapper)
        else:
            if image.color_id in data_ids:
                data.append({
                    "id": image.id,
                    'color': image.color_id
                })
                number = [d.get('count') for d in data if d['color'] == image.color_id]
                data[-1]['count'] = number[0] + 1
            else:
                data.append({
                    "id": image.id,
                    'count': 1,
                    'color': image.color_id
                })
                data_ids.append(image.color_id)
    filtered_data = sorted(data, key=lambda t: t.get('count'), reverse=True)
    result_data = []
    for i in filtered_data:
        if product.product_type == 'book':
            res = ProductImage.objects.filter(product_id=pk, wrapper__exact=i['wrapper']).first()
        else:
            res = ProductImage.objects.filter(product_id=pk, color_id=i['color']).first()
        if res not in result_data and res is not None:
            result_data.append(res)
    new_products = Product.objects.filter(~Q(id=product.id), is_active=True).order_by('-created_at')[:5]
    comments = Rate.objects.filter(product_id=pk).order_by('-id')
    category = Category.objects.filter(is_active=True)
    colors = Color.objects.all()
    if product.id:
        product.view += 1
        product.save()
    image_objects = ProductImage.objects.filter(product_id=pk, color=images[0].color)
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
    variants = Variant.objects.filter(product_type=product.product_type).order_by('duration')
    active_variant = variants.filter(product_type=product.product_type).last()
    total = image_objects.first().price_uzs + ((active_variant.percent * image_objects.first().price_uzs) / 100)
    _total = product.uzs_price + ((active_variant.percent * product.uzs_price) / 100)
    monthly = _total / active_variant.duration
    print(monthly)
    context = {
        'form': form,
        "colors": colors,
        "images": result_data,
        "image_objects": image_objects,
        "product": product,
        "variants": variants,
        "active_variant": active_variant,
        "default_monthly_price": int(monthly),
        "monthly": monthly,
        'comments': comments,
        "new_products": new_products,
        "categories": category,
        "related_products": related_products[:4],
    }
    return render(request, "shop-details.html", context)


def shop_images(request):
    data = []
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        product_id = request.POST.get('product_id')
        new_image = ProductImage.objects.get(id=image_id)
        images = ProductImage.objects.filter(product_id=product_id, color=new_image.color)
        for i in images:
            data.append({
                "url": i.image.url
            })

    return JsonResponse({"data": data})


class PorductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        qs = self.queryset.filter(~Q(id=product.id), is_active=True)
        data = ProductRetrieveSerializer(product, many=False).data
        footer = AppProductSerializer(qs.filter(category__in=[i.id for i in product.category.all()], ), many=True).data
        sidebar = AppProductSerializer(qs.order_by('-created_at')[:5], many=True).data
        variant = VariantSerializer(Variant.objects.filter(product_type=product.product_type), many=True).data

        return Response({'data': data, 'footer': footer, 'sidebar': sidebar, 'variant': variant})


def book_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    related_products = Product.objects.filter(~Q(id=product.id), category__in=[i.id for i in product.category.all()],
                                              is_active=True)
    images = ProductImage.objects.filter(product_id=pk)
    data = []
    data_ids = []
    for image in images:
        if image.wrapper in data_ids:
            data.append({
                "id": image.id,
                'wrapper': image.wrapper
            })
            number = [d.get('count') for d in data if d['wrapper'] == image.wrapper]
            data[-1]['count'] = number[0] + 1
        else:
            data.append({
                "id": image.id,
                'count': 1,
                'wrapper': image.wrapper
            })
            data_ids.append(image.wrapper)

    filtered_data = sorted(data, key=lambda t: t.get('count'), reverse=True)
    result_data = []
    for i in filtered_data:
        res = ProductImage.objects.filter(product_id=pk, wrapper__exact=i['wrapper']).first()
        if res not in result_data and res is not None:
            result_data.append(res)

    new_products = Product.objects.filter(~Q(id=product.id), is_active=True).order_by('-created_at')[:5]
    comments = Rate.objects.filter(product_id=pk).order_by('-id')
    category = Category.objects.filter(is_active=True)
    colors = Color.objects.all()
    if product.id:
        product.view += 1
        product.save()
    image_objects = ProductImage.objects.filter(product_id=pk, color=images[0].color)
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
    variants = Variant.objects.filter(product_type=product.product_type).order_by('duration')
    active_variant = variants.filter(product_type=product.product_type).last()
    total = image_objects.first().price_uzs + ((active_variant.percent * image_objects.first().price_uzs) / 100)
    monthly = total / active_variant.duration
    context = {
        'form': form,
        "colors": colors,
        "images": result_data,
        "image_objects": image_objects,
        "product": product,
        "variants": variants,
        "active_variant": active_variant,
        "default_monthly_price": int(monthly),
        'comments': comments,
        "new_products": new_products,
        "categories": category,
        "related_products": related_products[:4],
    }
    return render(request, "book-detail.html", context)
