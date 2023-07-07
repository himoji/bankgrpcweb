from flask import Blueprint, render_template, request, jsonify, redirect, url_for

bank_views = Blueprint("bank_views", __name__)
from . import client, main

#bank stuff
@bank_views.route("/atm")
def atmPage():
    args = request.args
    customer_name = args.get("customer_name")
    return render_template("atm/atm.html", customer_name = customer_name, customer_cash = main.atm.getCashAmount(main.atm.getCustomerId(customer_name)))

@bank_views.route("/deposit", methods=["GET", "POST"]) #type: ignore
def depositPage():
    args = request.args
    customer_name = args.get("customer_name")
    print(customer_name, main.atm.getCustomerId(customer_name), "\n\n\n\n\n\n\n\n\n")
    if request.method == 'POST':
        cash = request.form['cash']
        ci = main.atm.getCustomerId(customer_name)
        if client.rundeposit(ci, int(cash)): # type: ignore!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return redirect(url_for("auth_views.accountPage", customer_name = customer_name))
        else: 
            print(f"Deposit failed {cash}")
            return render_template("/atm/deposit.html", success="false")
    return render_template("/atm/deposit.html", customer_name = customer_name)

@bank_views.route("/withdraw", methods=["GET", "POST"]) #type: ignore
def withdrawPage():
    args = request.args
    customer_name = args.get("customer_name")
    if request.method == 'POST':
        cash = request.form['cash']
        if client.runwithdraw(main.atm.getCustomerId(customer_name), int(cash)): # type: ignore
            return redirect(url_for("auth_views.accountPage", customer_name = customer_name))
        else: 
            print("Withdraw failed")
            return render_template("/atm/withdraw.html", success="false")
    return render_template("/atm/withdraw.html", customer_name = customer_name)

@bank_views.route("/send", methods=["GET", "POST"]) #type: ignore
def sendPage():
    args = request.args
    customer_name = args.get("customer_name")
    if request.method == 'POST':
        cash = request.form['cash']
        taker = request.form['taker']
        if client.runsend(main.atm.getCustomerId(customer_name), int(cash), main.atm.getCustomerId(taker)): # type: ignore
            print("Sending...")
            return redirect(url_for("auth_views.accountPage", customer_name = customer_name))
        else: 
            print("Sending failed")
            return render_template("/atm/send.html", success="false")
    return render_template("/atm/send.html", customer_name = customer_name)