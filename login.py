from flask import Flask,session,redirect,render_template,url_for,request,abort,flash
from sqlalchemy import *
from sqlalchemy import String, ForeignKey,create_engine ,Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST','GET'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
        return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()