from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, jsonify
from models import storage
from models.product import Product, ProductImage
from flask_login import current_user
from models.user import User, UnAuthenticatedUser
from models.order import Order
from models import storage
import datetime
import json
from .utils import cookieCart, cartData, guestOrder

views = Blueprint('views', __name__)

@views.route('/store', methods=['GET', 'POST'])
def store():
    all_product = storage.all(Product)
    all_images = storage.all(ProductImage)

    total_quantity = None
    if current_user.is_authenticated:
        user_id = current_user.id
        total_quantity = Order.get_order_quant(user_id)
    else:
        cookieData = cookieCart(request)
        total_quantity = cookieData['cartItems']

    return render_template("store.html", all_product=all_product, all_images=all_images, currentUser=current_user, total_quantity=total_quantity)

@views.route('/selected_item/<productId>', methods=['GET'])
def selected_cart(productId):
    selectedItem = storage.get_user_by_id(Product, productId)
    all_images = storage.get_product_images(ProductImage, productId)
    total_quantity = 0
    if current_user.is_authenticated:
        user_id = current_user.id
        total_quantity = Order.get_order_quant(user_id)
    else:
        cookieData = cookieCart(request)
        total_quantity = cookieData['cartItems']
    return render_template("selected_item.html", total=total_quantity, selectedItem=selectedItem, productId=productId, all_images=all_images, user_id=current_user)


@views.route('/cart', methods=['GET'])
def cart():
    data = cartData(request, current_user)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    all_images = data['all_images']
    
    return render_template('cart.html', items=items, order=order, cartItems=cartItems,  all_images=all_images, currentUser=current_user)
    
@views.route('/checkout', methods=['GET'])
def checkout():
    data = cartData(request, current_user)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    all_images = data['all_images']

    return render_template('checkout.html', items=items, cartItems=cartItems, order=order, all_images=all_images, currentUser=current_user)

@views.route('/updateItem', methods=['POST'])
def updateItem():
    data = json.loads(request.data)
    productId = data.get('productId')
    action = data.get('action')
    productSize = data.get('productSize')
    productColor = data.get('productColor')
    if productId is None or action is None:
        return jsonify({'error': 'Missing productId or action'})

    newItem = storage.get_user_by_id(Product, productId)
    product = storage.get_orders_by_product_id(productId, current_user.id)

    if current_user.is_authenticated:
        if product:
            for item in product:
                if action == 'add':
                    item.productQuantity += 1
                    if productColor is not None or productSize is not None:
                        if item.productColor != productColor or item.productSize != productSize:
                            item.productColor = productColor 
                            item.productSize = productSize
                elif action == 'remove':
                    item.productQuantity -= 1
                    if item.productQuantity <= 0:
                        storage.delete(item)
            storage.save()
            return jsonify({'message': 'Orders updated successfully'})
        else:
            order = {
                'productName': newItem.BrandName,
                'productPrice': newItem.productPrice,
                'productQuantity': 1,
                'productSize': productSize,
                'productColor': productColor,
                'paymentStatus': 'pending',
                'user_id': current_user.id,
                'seller_id': newItem.seller_id, 
                'product_id': newItem.id,
            }
            newOrder = Order(**order)
            newOrder.save()
            return jsonify({'message': 'Orders added successfully'})
    else: 
        print('not authenticated')    
        return jsonify({'message': 'User not authenticated'})
    
@views.route('/processOrder', methods=['POST', 'GET'])
def processOrder():
    if request.method == 'POST':
        data = request.get_json()
        print('Data', data)
        transaction_id = datetime.datetime.now().timestamp()
        if current_user.is_authenticated:
            user_id = current_user.id
            total = data['form']['total']
            if total == Order.get_order_total(user_id):
                items = storage.get_orders_by_user_id(Order, user_id)
                if items:
                    for item in items:
                        item.paymentStatus = "paid"
                        item.transaction_id = transaction_id
                    storage.save()
        else:
            customer, order = guestOrder(request, data)
    return jsonify('payment complete')