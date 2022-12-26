from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()     
DB_NAME="database.db"       #name of database is stored in this variable



def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']="helloworld"                             #evry app has a secret key and in this case we defined it as helloworld
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    from .models import User  #Imports the user table from models.py
    with app.app_context():
        db.create_all()
        print("Created Database")
                                                    
    login_manager=LoginManager()            #Login Manager created
    login_manager.login_view="auth.login"  #if someone is not logged in we redirect them to auth.login
    login_manager.init_app(app)

    @login_manager.user_loader              #used to get information about username provided the id 
    def load_user(id):
        return User.query.get(int(id))

    return app

