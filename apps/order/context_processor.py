from .models import Cart, Wishlist
import uuid


def cart_renderer(request):
    try:
        cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
        wishlists = Wishlist.objects.filter(session_id=request.session['nonuser'])
    except:
        request.session['nonuser'] = str(uuid.uuid4())
        cart = Cart.objects.create(session_id=request.session['nonuser'])
        wishlists = None

    return {
        "cart": cart,
        "wishlists": wishlists
    }
