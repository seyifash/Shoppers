from flask import Flask
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from models.seller_user import Seller
from models.user import User
from itsdangerous.exc import SignatureExpired
from flask_mail import Mail
from models import storage
from decouple import config



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Ayomide'
    app.config['UPLOAD_FOLDER'] = r'store\static\uploads'
    app.config['MAIL_SERVER'] = config('MAIL_SERVER', default='smtp.gmail.com')
    app.config['MAIL_PORT'] = config('MAIL_PORT', default=465, cast=int)
    app.config['MAIL_USE_SSL'] = config('MAIL_USE_SSL', default=True, cast=bool)
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_SSL_VERSION'] = 'TLSv1.3'
    app.config['MAIL_USERNAME'] = 'nexuscorefortobi@gmail.com'
    app.config['MAIL_PASSWORD'] = 'quanbhgkggjiownn'
    
    mail = Mail(app)
    app.config['mail'] = mail
    
    
    from .views import views
    from .views import views
    from .seller_auth import seller_auth
    from .seller_views import seller_views
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(seller_auth, url_prefix='/')
    app.register_blueprint(seller_views, url_prefix='/')
    
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    app.config['serializer'] = serializer
    
    
    login_manager = LoginManager()
    login_manager.login_view = 'seller_auth.seller_login'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        user_classes = [Seller, User]  # Add more classes as needed

        for user_class in user_classes:
            user = storage.get_user_by_id(user_class, id)
            if user:
                return user
        return None
    
    return app 
    
    