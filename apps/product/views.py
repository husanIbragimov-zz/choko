from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from apps.product.forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from apps.order.models import Variant
from apps.product.models import Category, Banner, Brand, Product, Rate, Advertisement, Color, ProductImage, \
    BannerDiscount
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
    banner_discounts = BannerDiscount.objects.filter(is_active=True)
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

    for banner_discount in banner_discounts:
        now = timezone.now()
        deadline = banner_discount.deadline
        print(now)
        print(deadline)
        if now >= deadline:
            banner_discount.is_active = False
            banner_discount.save()

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
        'status_index': status_index,
        'banner_discounts': banner_discounts[:1],
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
    images = ProductImage.objects.raw(
        'SELECT *, count(color_id) as number_colors FROM product_productimage WHERE product_id = %s GROUP BY color_id ORDER By number_colors desc',
        [id])
    new_products = Product.objects.filter(~Q(id=product.id), is_active=True).order_by('-created_at')[:5]
    comments = Rate.objects.filter(product_id=id).order_by('-id')
    category = Category.objects.filter(is_active=True)
    colors = Color.objects.all()
    if product.id:
        product.view += 1
        product.save()
    image_objects = ProductImage.objects.filter(product_id=id, color=images[0].color)
    print(image_objects)
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
    variants = Variant.objects.all().order_by('duration')
    active_variant = variants.last()
    total = image_objects.first().price_uzs + ((active_variant.percent * image_objects.first().price_uzs) / 100)
    monthly = total / active_variant.duration
    context = {
        'form': form,
        "colors": colors,
        "images": images,
        "image_objects": image_objects,
        "product": product,
        "variants": variants,
        "active_variant": active_variant,
        "default_monthly_price": monthly,
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
