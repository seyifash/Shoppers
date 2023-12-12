from flask import Flask
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Ayomide'
    app.config['UPLOAD_FOLDER'] = r'website\static\uploads'
    
    from .views import views
    
    
    app.register_blueprint(views, url_prefix='/')
    
    
    login_manager = LoginManager()
    
    return app
    