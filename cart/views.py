from django.shortcuts import render, redirect, get_object_or_404
from buy.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# function to check if the session id creatied for customer on browser

def _cart_id(request):
    cart = request.session.session_key # checks if there is a session key in customer browser
    #condition to check if the cart exists:
    # if no cart, we'll create a session and assign to the cart_id
    if not cart:
        cart = request.session.create()
    # else w'll return cart(session_key)
    return cart

# importing the redirect
# Product model
# Cart and CartItem models

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    #getting the cart by id:
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()
    try: # adding cart item
        cart_item = CartItem.objects.get(product=product, cart = cart)
        if cart_item.product.available == True:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart:cart_detail') # the url



# cart details

def cart_detail(request, total = 0, counter = 0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter +=cart_item.quantity
    # from django.core.exceptions import ObjectDoesNotExist
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items =cart_items, total = total, counter = counter))




# cart remove cart items

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


# delete the item

def delete_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
