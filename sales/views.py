from django.shortcuts import render
from models import  Cart,Product
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse


def add_to_cart(request):
    """
    Add product to cart
    """
    product_id = int(request.POST['product_id'])

    # Checking if user already has cart in session
    # otherwise create a new cart for the user
    if 'cart_id' in request.session:
        cart_id = int(request.session['cart_id'])
        cart = Cart.get_cart(cart_id)
    else:
        cart = Cart.get_cart()
        request.session['cart_id'] = cart.id

    try:
        quantity = int(request.POST['quantity'])
        if quantity > 0:
            cart.add_item(product_id, quantity, request.user)
        else:
            raise ValueError()
    except ValueError:
        return HttpResponseBadRequest('Product quantity is not correct, please enter one or more products in numbers.')

    if request.is_ajax():

        return render(request, 'sales/cart_basket.html', {'cart': cart})

    #return HttpResponseRedirect(reverse('sales_checkout_cart'))
    return render(request, 'sales/cart_basket.html', {'cart': cart})