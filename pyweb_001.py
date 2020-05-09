from math import *

from flask import  (
    Flask,
    render_template,
    request,
    g,
    session,
    redirect,
    url_for
)
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import pymongo 
from pymongo import MongoClient 



### Tạo APP
app = Flask(__name__)
#, static_url_path='', static_folder='/static'
app.secret_key = "adtekdev"

### LIÊN KẾT TỚI DB MONGO
MONGO_URI = 'mongodb+srv://db01:csdl001@cluster0-eapdp.mongodb.net/test?retryWrites=true&w=majority'
cluster = MongoClient(MONGO_URI)

db =  cluster.ATN_Company  # cluster["ATN_Company"]


### CODE Flask - Python Web

@app.route('/')
def  index():
    return render_template("index.html")


@app.route('/home')
def  home():
    return render_template("home.html", username=session['username'], fullname=session['fullname'])

@app.route('/login', methods=['GET', 'POST'])
def  login():

    if session.get('logged_in_flag'):
        if session['logged_in_flag']:
            return redirect(url_for('home'))

    query_parameters = request.args
    vusername = query_parameters.get("username")
    vpassword = query_parameters.get("password")

    collection = db.account
    ### ch-eck Account / Tài khoản USER
    results = collection.find({"_id":vusername, "password": vpassword}) 


    if  results.count() == 1:
        session['logged_in_flag'] = True
        session['username'] = results[0]["_id"]
        session['fullname'] = results[0]["FullName"]
        return render_template("home.html", username=results[0]["_id"], fullname=results[0]["FullName"])
    else:
        session['logged_in_flag'] = False
        return render_template("login.html", mesg = "")

@app.route('/logout', methods=['GET', 'POST'])
def  logout():
    #if session.get('logged_in_flag'):
    if 'logged_in_flag' in session:
        session['logged_in_flag'] = False
    return ""

@app.route('/profile')
def  profile():
    return render_template("profile.html")

@app.route('/report')
def  report():
    return render_template("report.html")

@app.route('/addOrder')
def addOrder():
    if ("productName" in request.args  and "productAmount" in request.args and "productPrice" in request.args):
        pName = request.args.get("productName")
        pAmount = request.args.get("productAmount")
        pPrice = request.args.get("productPrice")
        newProduct = {"name" : pName, "amount" : pAmount, "price" : pPrice}
        collection = db.products 
        collection.insert_one(newProduct)
    return render_template("addOrder.html")

@app.route('/products', methods=['GET', 'POST'])
def products():
    collection = db.products 
    lpro = collection.find()
    return render_template("product-listA1.html", productList = lpro)

@app.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    if ("productName" in request.args  and "productPrice" in request.args):
        pName = request.args.get("productName")
        pPrice = request.args.get("productPrice")
        newProduct = {"name" : pName, "price" : pPrice}
        collection = db.products 
        collection.insert_one(newProduct)
    return render_template("addProduct.html")



 