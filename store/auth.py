from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from models.user import User
from models.product import Product, ProductImage
from models.order import Order
from models import storage
from hashlib import md5
import datetime
import json


auth = Blueprint('auth', __name__)

@auth.before_request
def before_request():
    storage.reload()  # Reload the database session before each request

@auth.teardown_request
def teardown_request(exception=None):
    storage.close()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = md5(password.encode()).hexdigest()
        existingUser = storage.get_by_email(User, email)
        if existingUser:
            if password2 == existingUser.password:
                login_user(existingUser)
                return redirect(url_for('auth.store'))
            else:
                flash('Incorrect password, try again', category='error') 
        else:
            flash('Email does not exist', category='error')      
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        existingUser = storage.get_by_email(User, email)
        if existingUser:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 3:
            flash('First name must be greater than 2 characters', category='error') 
        elif len(last_name) < 3:
            flash('Last name must be greater than 2 characters', category='error') 
        elif password != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password) < 4:
            flash('Passwords must be at least 4 characters', category='error')
        else:
            new_user = request.form.to_dict()
            new_user.pop('password2')
            created_user = User(**new_user)
            created_user.save()
            login_user(created_user) 
            return redirect(url_for('auth.mainViews', user_id=current_user.id))
    return render_template("signup.html")


@auth.route('/store', methods=['GET', 'POST'])
def store():
    all_product = storage.all(Product)
    all_images = storage.all(ProductImage)

    total_quantity = None
    if current_user.is_authenticated:
        user_id = current_user.id
        total_quantity = Order.get_order_quant(user_id)
    else:
        total_quantity = 0
    return render_template("store.html", all_product=all_product, all_images=all_images, currentUser=current_user, total_quantity=total_quantity)

@auth.route('/selected_item/<productId>', methods=['GET'])
def selected_cart(productId):
    selectedItem = storage.get_user_by_id(Product, productId)
    all_images = storage.get_product_images(ProductImage, productId)
    total_quantity = 0
    if current_user.is_authenticated:
        user_id = current_user.id
        total_quantity = Order.get_order_quant(user_id)
    return render_template("selected_item.html", total=total_quantity, selectedItem=selectedItem, productId=productId, all_images=all_images, user_id=current_user)

@auth.route('/cart', methods=['GET'])
def cart():
    items = None
    all_images = storage.all(ProductImage)
    if current_user.is_authenticated:
        user_id = current_user.id
        items = storage.get_orders_by_user_id(Order, user_id)
        total_amount = Order.get_order_total(user_id)
        total_quantity = Order.get_order_quant(user_id)
        order = {'get_all_total': total_amount, 'get_all_quantity': total_quantity}
        cartItems = order.get_all_quantity
    else:
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
                        'id': product.id,
                        'productName':product.productDescription,
                        'ProductPrice': product.productPrice,
                        'seller_id': product.seller_id,
                        'product_id': product.id,
                        'productSize': cart[i]["productSize"],
                        'productColor': cart[i]["productColor"],
                        'productPrice': product.productPrice,
                        'productQuantity': cart[i]["quantity"],
                        'get_total': total,
                }
                items.append(item)
            except:
                pass
                
    return render_template('cart.html', items=items, order=order, cartItems=cartItems,  all_images=all_images, currentUser=current_user)
@auth.route('/checkout', methods=['GET'])
def checkout():
    items = None
    all_images = storage.all(ProductImage)
    if current_user.is_authenticated:
        user_id = current_user.id
        items = storage.get_orders_by_user_id(Order, user_id)
        total_amount = Order.get_order_total(user_id)
        total_quantity = Order.get_order_quant(user_id)
        order = {'get_all_total': total_amount, 'get_all_quantity': total_quantity}
        cartItems = order.get_all_quantity
    else:
        try:
            cart = json.loads(request.cookies.get('cart'))
        except:
            cart = {}
        print('cart:', cart)
        items = []
        order = {'get_all_total': 0, 'get_all_quantity': 0}
        cartItems = order['get_all_quantity']
        for i in cart:
            cartItems += cart[i]["quantity"]
            product = storage.get_user_by_id(Product, i) 
            total = (product.productPrice * cart[i]['quantity'])
            order['get_all_total'] += total
            order['get_all_quantity'] += cart[i]["quantity"]
            item = {
                    'id': product.id,
                    'productName':product.productDescription,
                    'ProductPrice': product.productPrice,
                    'seller_id': product.seller_id,
                    'product_id': product.id,
                    'productSize': cart[i]["productSize"],
                    'productColor': cart[i]["productColor"],
                    'productPrice': product.productPrice,
                    'productQuantity': cart[i]["quantity"],
                    'paymentStatus': 'pending',
                    'transaction_id': None,
                    'get_total': total,
            }
            items.append(item)
                
    return render_template('checkout.html', items=items, cartItems=cartItems, order=order, all_images=all_images, currentUser=current_user)

@auth.route('/updateItem', methods=['POST'])
def updateItem():
    data = json.loads(request.data)
    productId = data.get('productId')
    action = data.get('action')
    productSize = data.get('productSize')
    productColor = data.get('productColor')
    print("productSize {}".format(productSize))
    print("productColor {}".format(productColor))
    
    if productId is None or action is None:
        return jsonify({'error': 'Missing productId or action'})

    newItem = storage.get_user_by_id(Product, productId)
    product = storage.get_orders_by_product_id(productId, current_user.id)
    print('all products:', product)

    if current_user.is_authenticated:
        if product:
            for item in product:
                print("item productSize {}".format(item.productSize))
                print("item productColor {}".format(item.productColor))
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
            return jsonify({'message': 'Orders updated successfully'})  # Return a valid response here
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
            print(newOrder)
            return jsonify({'message': 'Orders added successfully'})
    else: 
        print('not authenticated')    
        return jsonify({'message': 'User not authenticated'})
    
@auth.route('/processOrder', methods=['POST', 'GET'])
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
            
    return jsonify('payment complete')