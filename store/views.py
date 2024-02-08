"""from flask import Blueprint, render_template, request, jsonify, session
from models import storage
from models.product import Product, ProductImage

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def store():
    all_product = storage.all(Product)
    all_images = storage.all(ProductImage)
    for product in all_product.values():
        print("All product: {} ".format(product))
        for images in all_images.values():
            if images.product_id == product.id:
                print("All images:{}".format(images.image_filename))
                break
    return render_template("store.html", all_product=all_product, all_images=all_images)

@views.route('/selected_item/<productId>', methods=['GET'])
def selected_cart(productId):
    selectedItem = storage.get_user_by_id(Product, productId)
    all_images = storage.get_product_images(ProductImage, productId)
    if all_images:
        for images in all_images:
            print("All images:{}".format(images.image_filename))   
    else:
        print("no image")
    
    return render_template("selected_item.html", selectedItem=selectedItem, all_images=all_images)

@views.route('/cart')
def cart():
    return render_template("cart.html")

@views.route('/checkout', methods=['GET'])
def checkout():
    return render_template("checkout.html")
    """