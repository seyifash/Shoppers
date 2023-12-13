from flask import Blueprint, render_template, request, jsonify, session

views = Blueprint('views', __name__)

@views.route('/')
def store():
    return render_template("store.html")

@views.route('/selected_item')
def selected_cart():
    return render_template("selected_item.html")

@views.route('/cart')
def cart():
    return render_template("cart.html")

@views.route('/checkout', methods=['GET'])
def checkout():
    return render_template("checkout.html")