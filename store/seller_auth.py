from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from models.seller_user import Seller
from models import storage
from hashlib import md5


seller_auth = Blueprint('seller_auth', __name__)

@seller_auth.route('/seller_login', methods=['GET', 'POST'])
def seller_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = md5(password.encode()).hexdigest()
        existingUser = storage.get_by_email(Seller, email)
        if existingUser:
            if password2 == existingUser.password:
                login_user(existingUser)
                return redirect(url_for('seller_views.sellerViews'))
            else:
                flash('Incorrect password, try again', category='error') 
        else:
            flash('Email does not exist', category='error')      
    return render_template("seller_login.html")

@seller_auth.route('/seller_logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('seller_auth.seller_login'))

@seller_auth.route('/seller_sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        existingUser = storage.get_by_email(Seller, email)
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
            created_user = Seller(**new_user)
            created_user.save()
            login_user(created_user) 
            return redirect(url_for('seller_views.sellerViews'))
    return render_template("seller_signup.html")