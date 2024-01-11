from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from flask_login import current_user, login_user, logout_user, login_required
from models.seller_user import Seller
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
from models import storage
from hashlib import md5


seller_auth = Blueprint('seller_auth', __name__)



def send_confirmation_email(email):
    serializer = current_app.config['serializer']
    mail = current_app.config['mail'] 
    token = serializer.dumps(email, salt='seller-email-confirm')
    confirm_url = url_for('seller_auth.confirm_email', token=token, _external=True)
    msg = Message('Confirm Your Email', sender='oluwaseyiluxury@gmail.com', recipients=[email])
    msg.body = f'To confirm your email, click on the following link: {confirm_url}'
    mail.send(msg)
    

@seller_auth.route('/confirm_email/<token>', methods=['GET'])    
def confirm_email(token):
    serializer = current_app.config['serializer']
    try:
        email = serializer.loads(token, salt='seller-email-confirm', max_age=3600)
        user = storage.get_by_email(Seller, email)
        print(user)
        print(email)

        if user:
            print("my user: {}".format(user))
            try:
                user.confirm_email()
                storage.save()
                print("users again: {}".format(user))
                return redirect(url_for('seller_auth.seller_login'))
            except Exception as e:
                print(f"Error in confirm_email: {e}")
                return render_template('confirmation_errors.html')
        else:
            flash('User not found.', category='error')
            return render_template('confirmation_errors.html')
    except SignatureExpired:
        return render_template('confirmation_errors.html')
    except Exception as e:
        print(f"Error in confirm_email: {e}")
        return render_template('confirmation_error.html')

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
                print('you are getting in')
                return redirect(url_for('seller_views.sellers_dashboard'))
            else:
                flash('Incorrect password, try again', category='error') 
        else:
            flash('Email does not exist', category='error')      
    return render_template("seller_signin.html")

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
            send_confirmation_email(email)
            print("the users: {}".format(created_user))
            flash('A confirmation link has been sent to your email.', category='success')
    return render_template("seller_signup.html")