import json
from models.product import Product, ProductImage
from models.order import Order
from models.user import User, UnAuthenticatedUser
from models import storage

def cookieCart(request):
    try:
        cart = json.loads(request.cookies.get('cart'))
    except:
        cart = {}
    print('cart:', cart)
    items = []
    order = {'get_all_total': 0, 'get_all_quantity': 0}
    cartItems = order['get_all_quantity']
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = storage.get_user_by_id(Product, i) 
            total = (product.productPrice * cart[i]['quantity'])
            order['get_all_total'] += total
            order['get_all_quantity'] += cart[i]["quantity"]
            item = {
                    'user_id': None,
                    'productName':product.productDescription,
                    'ProductPrice': product.productPrice,
                    'seller_id': product.seller_id,
                    'product_id': product.id,
                    'productSize': cart[i]["productSize"],
                    'productColor': cart[i]["productColor"],
                    'productPrice': product.productPrice,
                    'productQuantity': cart[i]["quantity"],
                    'paymentStatus': 'pending',
                    'transaction_id': 0,
                    'get_total': total,
            }
            items.append(item)
        except:
            pass
            
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request, current_user):
    items = None
    all_images = storage.all(ProductImage)
    if current_user.is_authenticated:
        user_id = current_user.id
        items = storage.get_orders_by_user_id(Order, user_id)
        total_amount = Order.get_order_total(user_id)
        total_quantity = Order.get_order_quant(user_id)
        order = {'get_all_total': total_amount, 'get_all_quantity': total_quantity}
        cartItems = order['get_all_quantity']
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    return {'cartItems': cartItems, 'order': order, 'items': items, 'all_images': all_images}

def guestOrder(request, data):
    print('User is not logged in...')
    print('COOKIES:', json.loads(request.cookies.get('cart')))
    name = data['form']['name']
    names = name.split()
    first_name, last_name = names[0], names[1]
    email = data['form']['email']
    Address = data['form']['Address']
    phoneNumber = data['form']['phoneNumber']
    
    cookieData = cookieCart(request)
    total = data['form']['total']
    order = cookieData['order']
    items = cookieData['items']
    user_isNot = UnAuthenticatedUser(first_name=first_name, last_name=last_name, email=email, Address=Address, phoneNumber=phoneNumber)
    user_isNot.save()
    print(user_isNot.id)
    
    for item in items:
        item['user_id'] = user_isNot.id 
        orders = Order(**item)
        orders.save() 
        if total == order.get_all_total:
            items2 = storage.get_orders_by_user_id(Order, orders.user_id)
            if items2:
                for item in items2:
                    item.paymentStatus = "paid"
                    item.transaction_id = transaction_id
                storage.save() 
    return user_isNot, orders