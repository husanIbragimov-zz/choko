from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from apps.order.models import Cart, CartItem, Order, Wishlist
from apps.product.models import Product, Rate


# Create your views here.
def add_to_cart(request):
    if request.method == "POST":
        session_id = request.session['nonuser']
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']
        size = request.POST['size']
        cart = Cart.objects.get(session_id=session_id, completed=False)
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id)
        product = Product.objects.get(id=product_id)
        if cart_item.exists():
            for i in cart_item:
                i.quantity += int(quantity)
                i.save()
        else:
            if product.has_size:
                if size != '0':
                    cart_item = CartItem.objects.create(
                        cart_id=cart.id,
                        product_id=product_id,
                        quantity=quantity,
                        size=size
                    )
                    return JsonResponse({"msg": "Added to cart successfully!", "status": True})
                else:
                    return JsonResponse({"msg": "Please choose color!", "status": False})
            else:
                cart_item = CartItem.objects.create(
                    cart_id=cart.id,
                    product_id=product_id,
                    quantity=quantity
                )
                return JsonResponse({"msg": "Added to cart successfully!", "status": True})
    return JsonResponse({"msg": "Added to cart successfully!", "status": True})


@login_required(login_url='/login')
def create_order(request, id):
    cart = get_object_or_404(Cart, id=id)
    cart_items = cart.cart_items.all()
    user = request.user
    order = Order.objects.create(
        user=user
    )
    for item in cart_items:
        item.order = order
        item.save()
    cart.completed = True
    cart.save()
    return redirect('/')


@login_required(login_url='/login')
def review(request):
    rating = request.POST['rating']
    comment = request.POST['comment']
    product = request.POST['product']
    user = request.user

    rate = Rate.objects.create(
        user=user,
        product_id=product,
        comment=comment,
        rate=rating
    )
    return redirect(f'/shop-details/{product}')


def shop_cart(request):
    session_id = request.session['nonuser']
    cart = Cart.objects.filter(session_id=session_id, completed=False)
    context = {
        'cart': cart.last()
    }
    return render(request, "shop-cart.html", context)


def delete_cart_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.delete()
    return redirect('/order/shop-cart')


def wishlist(request, id):
    session_id = request.session['nonuser']
    product = get_object_or_404(Product, id=id)
    url = request.META.get('HTTP_REFERER')

    if Wishlist.objects.filter(session_id=session_id, product=product).exists():
        return redirect(url)
    else:
        wishlist = Wishlist.objects.create(
            session_id=session_id,
            product=product
        )
        return redirect(url)


def wishlist_list(request):
    return render(request, "shop-wishlist.html")


def delete_wishlist(request, id):
    Wishlist.objects.get(id=id).delete()
    url = request.META.get('HTTP_REFERER')
    return redirect(url)


def create_order_wishlist(request, id):
    product = Product.objects.get(id=id)
    session_id = request.session['nonuser']
    cart = Cart.objects.get(session_id=session_id, completed=False)
    cart_item = CartItem.objects.create(
        product=product,
        quantity=1,
        cart=cart

    )
    wishlist = Wishlist.objects.filter(session_id=session_id, product_id=id).delete()
    url = request.META.get('HTTP_REFERER')
    return redirect(url)
