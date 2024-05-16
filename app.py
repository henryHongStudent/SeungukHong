from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)


dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/campers", methods=['GET','POST'])
def campers():
    if request.method == "GET":
        return render_template("datepickercamper.html", currentdate = datetime.now().date())
    else:
        campDate = request.form.get('campdate')
        connection = getCursor()
        connection.execute("SELECT * FROM bookings join sites on site = site_id inner join customers on customer = customer_id where booking_date= %s;",(campDate,))
        camperList = connection.fetchall()
        return render_template("datepickercamper.html", camperlist = camperList)

@app.route("/booking", methods=['GET','POST'])
def booking():
    if request.method == "GET":
        return render_template("datepicker.html", currentdate = datetime.now().date())
    else:
        bookingNights = request.form.get('bookingnights')
        bookingDate = request.form.get('bookingdate')
        occupancy = request.form.get('occupancy')
        firstNight = date.fromisoformat(bookingDate)

        lastNight = firstNight + timedelta(days=int(bookingNights))
        connection = getCursor()
        connection.execute("SELECT * FROM customers;")
        customerList = connection.fetchall()
        connection.execute("select * from sites where occupancy >= %s AND site_id not in (select site from bookings where booking_date between %s AND %s);",(occupancy,firstNight,lastNight))
        siteList = connection.fetchall()
        print(type(siteList))
        return render_template("bookingform.html", customerlist = customerList, bookingdate=bookingDate, sitelist = siteList, bookingnights = bookingNights,occupancy= occupancy)    

@app.route("/booking/add", methods=['POST'])
def makebooking():
    if request.method == "POST":
        bookingDate_String=request.form.get("bookingdate")
        bookingDate_Obj=datetime.strptime(bookingDate_String, '%Y-%m-%d')
        bookingDate=bookingDate_Obj.date()
        customer=int(request.form.get("customer"))
        site=request.form.get("site")
        occupancy=int(request.form.get("occupancy"))
        connection = getCursor()
        connection.execute("INSERT INTO bookings (booking_date, customer, site, occupancy) VALUES (%s, %s, %s, %s);",(bookingDate,customer,site,occupancy))
        connection.close()
        return redirect(url_for('booking'))
    
@app.route("/camperlist", methods=['GET'])
def camperList():
    if request.method == "GET":
        connection = getCursor()
        connection.execute("SELECT bookings.*, customers.firstname, customers.familyname FROM bookings INNER JOIN customers ON bookings.customer = customers.customer_id; ")
        camperList=connection.fetchall()
        print(type(camperList))
        return render_template("camperlist.html", camperList = camperList)
        # return camperList

@app.route("/customer", methods=['GET','POST'])
def customerList():
    if request.method == "GET":
        connection = getCursor()
        connection.execute("SELECT * FROM customers;")
        customerList = connection.fetchall()
        return render_template("customer.html", customerlist = customerList)
@app.route("/customer/add", methods=['POST','GET'])
def addCustomer():
    if request.method=="GET":
        return render_template("addcustomer.html")
    else :
        firstname =request.form.get("firstname")
        familyname = request.form.get("familyname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        connection = getCursor()
        connection.execute("INSERT INTO customers (firstname, familyname, email, phone) VALUES (%s, %s, %s, %s);",(firstname,familyname,email,phone))
        connection.close()
        return redirect(url_for('customerList'))
            
@app.route("/customer/result", methods=['GET'])    
def searchResult():
    if request.method == "GET":
        searchString = request.args.get("search").capitalize()
        connection = getCursor()
        connection.execute("SELECT * FROM customers WHERE firstname LIKE %s OR familyname LIKE %s OR customer_id LIKE %s OR email LIKE %s OR phone LIKE %s ;",('%'+searchString+'%', '%'+searchString+'%','%'+searchString+'%','%'+searchString+'%','%'+searchString+'%'))
        customerList = connection.fetchall()
        return  render_template("customer.html", customerlist = customerList)


