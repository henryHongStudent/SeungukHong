from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from mysql.connector import FieldType
import connect
import re   # this is for validate  and phone number
app = Flask(__name__)
dbconn = None
connection = None
phonevalidation= re.compile(r'^\d{9,10}$') # This regex code validates phone numbers, accepting only 9 or 10 digits.
def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, 
    password=connect.dbpass, host=connect.dbhost, 
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

#booking page 
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
        customer = connection.fetchall()
        connection.execute("select * from sites where occupancy >= %s AND site_id not in (select site from bookings where booking_date between %s AND %s);",(occupancy,firstNight,lastNight))
        siteList = connection.fetchall()
        connection.close()  
        return render_template("bookingform.html", customer = customer, bookingdate=bookingDate, sitelist = siteList, bookingnights = bookingNights,occupancy= occupancy)    

#booking add page
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
        #Insert data to database.
        connection.close()
        return render_template("bookingconfirmation.html")

#Display camper list page
@app.route("/camperlist", methods=['GET'])
def camperList():
    if request.method == "GET":
        connection = getCursor()
        connection.execute("SELECT bookings.*, customers.firstname, customers.familyname FROM bookings INNER JOIN customers ON bookings.customer = customers.customer_id; ")
        #The query joins the bookings and customers tables to retrieve information from both tables, including customer names.
        camperList=connection.fetchall() # camperList stores the result of the fetchall.
        connection.close() 
        return render_template("camperlist.html", camperList = camperList) # send camperlist to camperlist.html as parameter.
      

#Display customer list page
@app.route("/customer", methods=['GET','POST'])
def customerList():
    if request.method == "GET":
        connection = getCursor()
        connection.execute("SELECT * FROM customers;")
        #The query selects all data from the customers table.
        customer = connection.fetchall() # customer stores the result of the fetchall.
        connection.close() 
        return render_template("customer.html", customer = customer) # send customer to customer.html as parameter.

#Add customer page
@app.route("/customer/add", methods=['POST','GET'])
def addCustomer():
    if request.method=="GET":
        return render_template("addcustomer.html")
    else :
        firstname =request.form.get("firstname")
        familyname = request.form.get("familyname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        if not phonevalidation.match(phone): #If the phone number is not in the correct format, an error message will be displayed.
            phone_error_message="Please enter correct phone number format ex: length 9~10 only numbers."
            return render_template("addcustomer.html",phone_error_message=phone_error_message)
            #send error message to addcustomer.html
        connection = getCursor()
        connection.execute("INSERT INTO customers (firstname, familyname, email, phone) VALUES (%s, %s, %s, %s);",(firstname,familyname,email,phone))
        connection.close()
        return render_template("addcustomerconfirmation.html")

#Display search result page
@app.route("/customer/result", methods=['GET'])    
def searchResult():
    if request.method == "GET":
        searchString = request.args.get("search").capitalize() 
        #Convert the search string to lowercase for case-insensitive searching.
        connection = getCursor()
        connection.execute("SELECT * FROM customers WHERE firstname LIKE %s OR familyname LIKE %s OR customer_id LIKE %s OR email LIKE %s OR phone LIKE %s ;",('%'+searchString+'%', '%'+searchString+'%','%'+searchString+'%','%'+searchString+'%','%'+searchString+'%'))
        customer = connection.fetchall()
        connection.close() 
        return  render_template("customer.html", customer = customer)

#Update selected customer information page
@app.route("/customer/update?customer_id=<customer_id>", methods=['POST','GET'])
def updateCustomer(customer_id):
    if request.method=="GET":
        connection = getCursor()
        connection.execute("SELECT * FROM customers WHERE customer_id = %s;",(customer_id,))
        #use customer_id to get one selected customer information.
        selectedCustomer = connection.fetchone()
        #fetchone() return one selected customer information and store it in selectedCustomer.
        return render_template("updatecustomer.html",customer_id=selectedCustomer[0], firstname = selectedCustomer[1], familyname = selectedCustomer[2], email = selectedCustomer[3], phone = selectedCustomer[4])
    else:
        customer_id = request.form.get("customer_id")
        firstname =request.form.get("firstname")
        familyname = request.form.get("familyname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        connection = getCursor()
        connection.execute("UPDATE customers SET firstname = %s, familyname = %s, email = %s, phone = %s WHERE customer_id = %s;",(firstname,familyname,email,phone,customer_id))
        connection.close()
        return render_template("updatedcustomerconfirmation.html")    

#Display report page
@app.route("/report", methods=['GET'])
def report():
    if request.method == "GET":
        connection = getCursor()
        connection.execute('''SELECT 
                                CONCAT(customers.firstname, ' ', customers.familyname) AS Customer_Name,
                                COUNT(*) AS Total_booking,
                                AVG(bookings.occupancy) AS avg_occupancy
                            FROM 
                                bookings
                            INNER JOIN 
                                customers ON bookings.customer = customers.customer_id
                            GROUP BY 
                                CONCAT(customers.firstname, ' ', customers.familyname);''')
        #This query joins the bookings table and the customers table to calculate the total number of bookings and average occupancy for each customer, grouping the results 
        # by the concatenated full name.
        report = connection.fetchall()
        connection.close() 
        return render_template("report.html", report = report)

