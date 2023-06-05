from .cart_ import Cart

def cart(request):
    return {'cart':Cart(request)}
