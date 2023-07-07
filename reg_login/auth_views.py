from flask import Blueprint, render_template, request, jsonify, redirect, url_for

auth_views = Blueprint("auth_views", __name__)
from . import client

#account management stuff
@auth_views.route("/login", methods=["GET", "POST"]) #type: ignore
def loginPage():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_password = request.form['customer_password']
        if client.runlogin(customer_name, customer_password) != "false": # type: ignore
            return redirect(url_for("auth_views.accountPage", customer_name = customer_name))
        else: 
            print("Login failed")
            return render_template("web/login.html", success="false")
    return render_template("web/login.html")

@auth_views.route("/register", methods=["GET", "POST"]) #type: ignore
def registerPage():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_password = request.form['customer_password']
        if client.runregister(customer_name, customer_password) != "false": # type: ignore
            return redirect(url_for("auth_views.accountPage", customer_name = customer_name))
        else: 
            print("Registration failed")
            return render_template("web/register.html", success="false")
    return render_template("web/register.html")

@auth_views.route("/account")
def accountPage():
    args = request.args
    customer_name = args.get("customer_name")
    return redirect(url_for("bank_views.atmPage", customer_name = customer_name))