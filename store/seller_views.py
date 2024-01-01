from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from models.product import Product
from models.product import ProductImage
from models.categories import Category
from werkzeug.utils import secure_filename
import os
from models import storage

seller_views = Blueprint('seller_views', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@seller_views.route('/seller')
def home():
    return render_template("seller_home.html")

@seller_views.route('/seller_upload', methods=['GET', 'POST'])
@login_required
def sellerViews():
    if request.method == 'POST' and current_user.is_authenticated:
        new_product = request.form.to_dict()
        if 'productImage' in request.files:
            uploaded_file = request.files['productImage']
            if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                # Save the file to a folder
                uploaded_file.save(file_path)
                # Set the 'productImage' field to the file path
                new_product['productImage'] = file_path
            else:
                flash('Invalid or missing file. Please upload a valid image file.', category='error')
            new_product['seller_id'] = current_user.id
            created_product = Product(**new_product)
            print(created_product)
            created_product.save()
    return render_template('seller.html')

@seller_views.route('/seller_dashboard', methods=['GET', 'POST'])
def sellers_dashboard():
    return render_template('sellers_dashboard.html')

@seller_views.route('/seller_orders', methods=['GET', 'POST'])
def sellers_orders():
    return render_template('sellers_orders.html')

@seller_views.route('/seller_customer', methods=['GET', 'POST'])
def sellers_customer():
    return render_template('sellers_customer.html')

@seller_views.route('/seller_uploads', methods=['GET', 'POST'])
def sellers_uploads():
    if request.method == 'POST' and current_user.is_authenticated:
        new_product = request.form.to_dict()
        
        if 'productCategory' in new_product:
            category_name = new_product['productCategory']

            # Check if the category already exists
            existing_categories = storage.all(Category)

            existing_category = None
            for category in existing_categories.values():
                if category.name == category_name:
                    existing_category = category
                    break

            if existing_category:
                # If the category already exists, use it
                new_category = existing_category
                print(new_category)
            else:
                # If the category doesn't exist, create a new one
                new_category = Category(name=category_name)
                new_category.save()
                print(new_category)
                
            new_product['category'] = new_category
        new_product['seller_id'] = current_user.id
        created_product = Product(**new_product)
        print(created_product)
        created_product.save()
        product_id = created_product.id
        if 'productImage' in request.files:
            uploaded_files = request.files.getlist['productImage']
            for uploaded_file in uploaded_files:
                if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
                    filename = secure_filename(uploaded_file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    # Save the file to a folder
                    uploaded_file.save(file_path)
                    # Set the 'productImage' field to the file path
                    new_image = ProductImage(product_id=product_id, image_filename=file_path)
                    new_image.save
                else:
                    flash('Invalid or missing file. Please upload a valid image file.', category='error')
    return render_template('sellers_upload.html')