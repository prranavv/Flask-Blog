from flask import Blueprint, render_template,redirect,url_for, request,flash
from .import db
from .models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth=Blueprint("auth",__name__)

@auth.route("/login", methods=['GET','POST'])
def login():
    email=request.form.get("email")
    password=request.form.get("password")
    return render_template("login.html")

@auth.route("/signup", methods=['GET','POST'])    #the get and post method is used to get or post links. ex when i submit my name in a form it has to be stored and posted on the server
def sign_in():
    if request.method == 'POST':
        username=request.form.get("username")
        email=request.form.get("email")
        password1=request.form.get("password1")
        password2=request.form.get("password2")

        email_exists=User.query.filter_by(email=email).first()
        username_exists=User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use', category='error')
        
        elif username_exists:
            flash('Username is already in use', category='error')
        
        elif password1!=password2:
            flash('Password don\'t match',category='error')

        elif len(username)<2:
            flash('Username is too short',category='error')
        
        elif len(password1)<6:
            flash('Password is too short',category='error')

        elif len(email)<4:
            flash('Email is invalid',category='error')

        else:
            new_user=User(email=email,username=username,password=password1)
            db.session.add(new_user)    #add the new user to the staging area like in git
            db.session.commit()         #adds the new user to the database
            flash('User created!')
            return redirect(url_for('views.home'))
    return render_template("signup.html")

@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))
