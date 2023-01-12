from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}

# In settings context processors section we should use name of the function
# In templates we should use the key of dictionary to access the value
