from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from apps.order.models import Cart, CartItem


# Create your views here.
def add_to_cart(request):
    if request.method == "POST":
        session_id = request.session['nonuser']
        product_id = request.POST['product_id']
        quantity = request.POST['quantity']
        cart = Cart.objects.get(session_id=session_id, completed=False)
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id)
        if cart_item.exists():
            for i in cart_item:
                i.quantity += int(quantity)
                i.save()
        else:
            cart_item = CartItem.objects.create(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity
            )
        messages.success(request, "Added to cart successfully!")
    return HttpResponse("Success")
