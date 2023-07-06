from flask import Blueprint, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, "views")
import client

#account management stuff
@views.route("/login", methods=["GET", "POST"]) #type: ignore
def loginPage():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_password = request.form['customer_password']
        if client.runlogin(customer_name, customer_password) != "false": # type: ignore
            return redirect(url_for("views.accountPage", customer_name = customer_name))
        else: 
            print("Login failed")
            return render_template("web/login.html", success="false")
    return render_template("web/login.html")

@views.route("/register", methods=["GET", "POST"]) #type: ignore
def registerPage():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_password = request.form['customer_password']
        if client.runregister(customer_name, customer_password) != "false": # type: ignore
            return redirect(url_for("views.accountPage", customer_name = customer_name))
        else: 
            print("Registration failed")
            return render_template("web/register.html", success="false")
    return render_template("web/register.html")

@views.route("/account")
def accountPage():
    args = request.args
    customer_name = args.get("customer_name")
    return render_template("web/account.html", customer_name = customer_name)