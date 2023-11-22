from django.db.models import Min
from .models import Cart, Wishlist
import uuid
from apps.contact.models import Subscribe
from ..base.models import Variant
from django.http import JsonResponse
from ..product.models import Currency, Category, Product, ProductImage


def ajax_renderer(request):
    if request.method == 'POST':
        # Retrieve data from the request
        min_value = request.POST.get('min')
        max_value = request.POST.get('max')

        products = Product.objects.filter(product_images__price__gte=min_value,
                                          product_images__price__lte=max_value).distinct()
        product_list = []
        for product in products:
            product_data = {
                'name': product.name,
                'price': product.price,
                # Add other fields as needed
            }
            product_list.append(product_data)

        context = {
            'products': product_list,
        }
        return JsonResponse(context, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def cart_renderer(request):
    currency = Currency.objects.last()
    categories = Category.objects.filter(is_active=True)
    sbb = request.POST.get('sbb')
    subscribe = Subscribe.objects.filter(email=sbb)
    variants = Variant.objects.all().order_by('duration')
    max_price = Product.objects.latest('uzs_price')
    min_price = Product.objects.earliest('uzs_price')
    active_variant = variants.last()
    if not subscribe.exists():
        if request.method == 'POST':
            Subscribe.objects.create(email=sbb)
    try:
        cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
        wishlists = Wishlist.objects.filter(session_id=request.session['nonuser'])
    except:
        request.session['nonuser'] = str(uuid.uuid4())
        cart = Cart.objects.create(session_id=request.session['nonuser'])
        wishlists = None

    return {
        "cart": cart,
        "active_variant": active_variant,
        "wishlists": wishlists,
        "currency": currency,
        'categories': categories,
        'max_price': max_price,
        'min_price': min_price,
    }
