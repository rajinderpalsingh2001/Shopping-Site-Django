from django.core.files.storage import FileSystemStorage
from django.http import *
from django.shortcuts import *
import sqlite3
from django.views.decorators.csrf import *
from datetime import datetime
import random


def getorders(request):
    conn = sqlite3.connect("db.sqlite3")
    s = "select * from 'order' where status='" + request.GET["q"] + "'"
    cr = conn.cursor()
    cr.execute(s)
    ans = cr.fetchall()

    p = "<table class='table'>"
    for row in ans:
        p = p + "<tr>"
        p = p + "<td>" + str(row[0]) + "</td>"
        p = p + "<td>" + str(row[1]) + "</td>"
        p = p + "<td>" + str(row[2]) + "</td>"
        p = p + "<td>" + str(row[3]) + "</td>"
        p = p + "<td>" + str(row[4]) + "</td>"
        p = p + "<td><a href='getdetails'>View Order Details</a></td>"
        p = p + "<td><a href='Ship Order'>Ship Order</a></td>"
        p = p + "</tr>"
    p = p + "</table>"

    return HttpResponse(p)


def vieworders(request):
    return render(request, "vieworders.html")


@csrf_exempt
def ordersuccess(request):
    del request.session["data"]

    d = {"ordernumber": request.POST["textbox1"]}

    conn = sqlite3.connect("db.sqlite3")
    cr = conn.cursor()

    s = "update 'order' set status='Payment Recieved' where ordernumber=" + request.POST["textbox1"]

    cr.execute(s)

    return render(request, "ordersuccess.html", {"ar": d})


def orderfailure(request):
    return render(request, "orderfailure.html")


@csrf_exempt
def makepayment(request):
    conn = sqlite3.connect("db.sqlite3")
    cr = conn.cursor()

    s = "select ordernumber from order_seq"
    cr.execute(s)
    ans = cr.fetchone()

    ordernumber = int(ans[0])
    ordernumber = ordernumber + 1

    s = "update order_seq set ordernumber=" + str(ordernumber)
    cr.execute(s)
    conn.commit()

    cartdata = list(request.session["data"])
    grandtotal = 0
    for row in cartdata:
        p = "insert into order_details values(NULL," + str(row["pid"]) + "," + str(row["qty"]) + "," + str(
            row["price"]) + "," + str(row["subtotal"]) + "," + str(ordernumber) + ")"
        cr.execute(p)
        grandtotal = grandtotal + row["subtotal"]
    conn.commit()

    x = datetime.now()

    s = "insert into 'order' values(" + str(ordernumber) + ",'" + str(x) + "','" + request.POST["fullname"] + "','" + \
        request.POST["address"] + "','" + request.POST["mobile"] + "','" + request.POST["email"] + "'," + str(
        grandtotal) + ",'Payment Pending',' ')"
    print(s)
    cr.execute(s)
    conn.commit()
    d = {"ordernumber": ordernumber, "total": grandtotal}
    return render(request, "makepayment.html", {"ar": d})


def checkout(request):
    return render(request, "checkout.html")


def resetsession(request):
    del request.session["data"]
    return HttpResponse("Session Reset")


def getcart(request):
    if "data" in request.session:
        x = list(request.session["data"])
    else:
        return HttpResponseRedirect("shopperhome")

    s = "<table class='table table-bordered table-sm table-striped' >"
    s+="<thead>"
    s+="<tr>"
    s+="<th>Sr.no</th>"
    s+="<th>Product Name</th>"
    s+="<th>Product Price</th>"
    s+="<th>Product Qty</th>"
    s+="<th>Net Price</th>"
    s+="</tr>"
    s+="</thead>"
    i = 1
    for row in x:
        s = s + "<tr>"
        s = s + "<td>" + str(i) + "</td>"
        s = s + "<td>" + str(row["pname"]) + "</td>"
        s = s + "<td>" + str(row["price"]) + "</td>"
        s = s + "<td>" + str(row["qty"]) + "</td>"
        s = s + "<td>" + str(row["subtotal"]) + "</td>"
        s = s + "</tr>"
        i+=1
    return HttpResponse(s)


def cart_total(request):
    if "data" in request.session:
        x = list(request.session["data"])
        total = 0
        for item in x:
            total = total + int(item["price"]) * int(item["qty"])
    else:
        total = 0

    return HttpResponse(total)


def cart(request):
    if "data" in request.session:
        x = list(request.session["data"])
    else:
        x = []
    conn = sqlite3.connect("db.sqlite3")
    s = "select * from products where pid=" + request.GET["q"]
    cr = conn.cursor()
    cr.execute(s)
    ans = cr.fetchone()

    flag = False
    print(x)
    for element in x:
        if element["pid"] == ans[0]:
            element["qty"] = int(element["qty"]) + 1
            element["subtotal"] = int(element["price"]) * int(element["qty"])
            flag = True

    if flag == False:
        d = {"pid": ans[0], "pname": ans[1], "price": ans[2], "photo": ans[5], "qty": 1, "subtotal": ans[2]}
        x.append(d)
    request.session["data"] = x
    return render(request, "cart.html", {"ar": x})


def getcategory(request):
    conn = sqlite3.connect("db.sqlite3")
    s = "select * from category"

    cr = conn.cursor()
    cr.execute(s)

    ans = cr.fetchall()

    p = "<li class='nav-item active mr-lg-2 mb-lg-0 mb-2'><a class='nav-link' href='shopperhomepage'>Home</a></li>"
    for row in ans:
        p = p + "<li class='nav-item active mr-lg-2 mb-lg-0 mb-2'><a class='nav-link' href='categorypage?q=categorypage?q="+row[0]+"'>" + row[0] + "</a></li>"
    return HttpResponse(p)


def selectcategory(request):
    conn = sqlite3.connect("db.sqlite3")
    s = "select * from products where catname='" + request.GET["q"] + "'"

    cr = conn.cursor()
    cr.execute(s)
    ans = cr.fetchall()

    p = "<div class='row'>"
    i = 0
    for row in ans:
        if i % 3 == 0:
            p = p + "</div>"
            p = p + "<div class='row'>"
        p = p + "<div class='col-sm-4'>"
        p = p + "<img src='static/media/" + row[5] + "' style='width:250px;height:250px'/>" + "<br>"
        p = p + "<h3>" + row[1] + "</h3>"
        p = p + str(row[2])
        p = p + "<a href='cart?q=" + str(row[0]) + "'><img src='/static/add.jpg' style='width:200px;height:100px'></a>"
        p = p + "</div>"
        i = i + 1
    p = p + "</div>"

    return HttpResponse(p)


def categorypage(request):
    conn = sqlite3.connect("db.sqlite3")
    s = "select * from products where catname='" + request.GET["q"] + "'"

    cr = conn.cursor()
    cr.execute(s)
    ans = cr.fetchall()

    x = []
    for row in ans:
        d = {"photo": row[5], "pname": row[1], "price": row[2]}
        x.append(d)

    return render(request, "categorypage.html", {"ar": x})


def shopperhomepage(request):
    conn = sqlite3.connect("db.sqlite3")
    s = "select * from category"

    cr = conn.cursor()
    cr.execute(s)
    ans = cr.fetchall()

    x = []
    for row in ans:
        d = {"catname": row[0]}
        x.append(d)

    return render(request, "shopperhomepage.html", {"ar": x})


def viewproducts(request):
    if not "username" in request.session:
        return HttpResponseRedirect("login")

    conn = sqlite3.connect("db.sqlite3")
    s = "select * from products"

    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    x = []
    for row in result:
        d = {"pid":row[0],"pname": row[1], "price": row[2], "description": row[3], "catname": row[4], "photo": row[5]}
        x.append(d)
    return render(request, "viewproducts.html", {"ar": x})


@csrf_exempt
def newproduct(request):
    if not "username" in request.session:
        return HttpResponseRedirect("login")

    # Step1 upload Photo
    obj = request.FILES['photo']
    path = "productphoto/" + str(random.randint(1, 1000)) + obj.name
    fs = FileSystemStorage()
    fs.save(path, obj)

    # Step2 Insert Data

    conn = sqlite3.connect("db.sqlite3")
    s = "insert into products values(NULL,'" + request.POST["pname"] + "'," + request.POST["price"] + ",'" + \
        request.POST["description"] + "','" + request.POST["catname"] + "','" + path + "')"
    cr = conn.cursor()
    cr.execute(s)
    conn.commit()
    return render(request, "newproduct.html", {"ar": "Product Added Successfully"})


def addproduct(request):
    if not "username" in request.session:
        return HttpResponseRedirect("login")
    conn = sqlite3.connect("db.sqlite3")
    s = "select * from category"
    cr = conn.cursor()
    cr.execute(s)
    ans = cr.fetchall()

    x = []
    for row in ans:
        d = {"catname": row[0]}
        x.append(d)

    return render(request, "addproduct.html", {"ar": x})


def logout(request):
    del request.session["username"]
    return HttpResponseRedirect("login")


def dashboard(request):
    if "username" in request.session:

        return render(request, "dashboard.html")
    else:
        return HttpResponseRedirect("login")


def checklogin(request):
    conn = sqlite3.connect("db.sqlite3")
    s = "select * from admin"
    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    flag = False
    for row in result:
        if row[0] == request.POST["textbox1"] and row[1] == request.POST["textbox2"]:
            flag = True
            break

    if flag == True:
        request.session["username"] = request.POST["textbox1"]
        return HttpResponseRedirect("dashboard")
    else:
        d = {"msg": "Login Failed"}

    return render(request, "checklogin.html", {"ar": d})


def login(request):
    return render(request, "login.html")


@csrf_exempt
def newadmin(request):
    if not "username" in request.session:
        return HttpResponseRedirect("login")

    conn = sqlite3.connect("db.sqlite3")

    s = "insert into admin  values('" + request.POST["textbox1"] + "','" + request.POST["textbox2"] + "','" + \
        request.POST["sel1"] + "','" + request.POST["textbox3"] + "')"

    cr = conn.cursor()
    cr.execute(s)

    conn.commit()

    d = {"msg": "Admin Added Successfully"}

    return render(request, "newadmin.html", {"ar": d})


def addadmin(request):
    if not "username" in request.session:
        return HttpResponseRedirect("login")

    return render(request, "addadmin.html")


def viewcategory(request):
    if not "username" in request.session:
        return HttpResponseRedirect("login")

    conn = sqlite3.connect("db.sqlite3")
    s = "select * from category"

    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    x = []
    for row in result:
        d = {"catname": row[0], "description": row[1]}
        x.append(d)
    return render(request, "viewcategory.html", {"ar": x})


def viewadmin(request):
    if not "username" in request.session:
        return HttpResponseRedirect("login")

    conn = sqlite3.connect("db.sqlite3")
    s = "select * from admin"

    cr = conn.cursor()
    cr.execute(s)
    result = cr.fetchall()
    x = []
    i = 1
    for row in result:
        d = {"count": i, "email": row[0], "type": row[2], "mobilenumber": row[3]}
        x.append(d)
        i += 1
    return render(request, "viewadmin.html", {"ar": x})


def addcategory(request):
    if not "username" in request.session:
        return HttpResponseRedirect("login")

    return render(request, "addcategory.html")


@csrf_exempt
def newcategory(request):
    if not "username" in request.session:
        return HttpResponseRedirect("login")

    conn = sqlite3.connect("db.sqlite3")
    cr = conn.cursor()

    p = "select * from category"
    cr.execute(p)
    result = cr.fetchall()

    x = False

    for row in result:
        if str(row[0]).upper() == str(request.POST["textbox1"]).upper():
            x = True
            break

    if x == False:
        s = "insert into category values('" + request.POST["textbox1"] + "','" + request.POST["textbox2"] + "')"
        cr.execute(s)
        conn.commit()
        d = {"msg": "New Category Added Successfully"}
    else:
        d = {"msg": "Duplicate Category name"}

    return render(request, "newcategory.html", {"ar": d})
