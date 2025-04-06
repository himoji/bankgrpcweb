from flask import Blueprint, render_template, request, redirect, url_for

bank_views = Blueprint("bank_views", __name__)
from . import Bankclient, main

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
    ci = main.atm.getCustomerId(customer_name)
    if request.method == 'POST':
        cash = request.form['cash']
        if Bankclient.rundepositClient(ci, int(cash)): # type: ignore!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
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
        if Bankclient.runwithdrawClient(main.atm.getCustomerId(customer_name), int(cash)): # type: ignore
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
        if Bankclient.runsendClient(main.atm.getCustomerId(customer_name), int(cash), main.atm.getCustomerId(taker)): # type: ignore
            print("Sending...")
            return redirect(url_for("auth_views.accountPage", customer_name = customer_name))
        else: 
            print("Sending failed")
            return render_template("/atm/send.html", success="false")
    return render_template("/atm/send.html", customer_name = customer_name)

# Investment features
@bank_views.route("/investments")
def investmentsPage():
    args = request.args
    customer_name = args.get("customer_name")
    portfolio = main.investment.getPortfolio(customer_name)
    return render_template("/investments/portfolio.html", customer_name=customer_name, portfolio=portfolio)

@bank_views.route("/investments/stocks", methods=["GET", "POST"])
def stocksPage():
    args = request.args
    customer_name = args.get("customer_name")
    # Get available stocks for display
    cursor = main.db.cursor()
    cursor.execute("SELECT symbol, name, price FROM stocks_table;")
    available_stocks = cursor.fetchall()
    cursor.close()
    
    if request.method == 'POST':
        action = request.form.get('action')
        stock_symbol = request.form.get('stock_symbol')
        amount = request.form.get('amount')
        
        if action == 'buy':
            if main.investment.buyStock(customer_name, stock_symbol, amount):
                return redirect(url_for("bank_views.investmentsPage", customer_name=customer_name))
            else:
                return render_template("/investments/stocks.html", customer_name=customer_name, 
                                     available_stocks=available_stocks, error="Failed to buy stock")
        elif action == 'sell':
            if main.investment.sellStock(customer_name, stock_symbol, amount):
                return redirect(url_for("bank_views.investmentsPage", customer_name=customer_name))
            else:
                return render_template("/investments/stocks.html", customer_name=customer_name, 
                                     available_stocks=available_stocks, error="Failed to sell stock")
    
    return render_template("/investments/stocks.html", customer_name=customer_name, available_stocks=available_stocks)

@bank_views.route("/investments/bonds", methods=["GET", "POST"])
def bondsPage():
    args = request.args
    customer_name = args.get("customer_name")
    # Get available bonds for display
    cursor = main.db.cursor()
    cursor.execute("SELECT bond_id, name, price, yield, maturity FROM bonds_table;")
    available_bonds = cursor.fetchall()
    cursor.close()
    
    if request.method == 'POST':
        action = request.form.get('action')
        bond_id = request.form.get('bond_id')
        amount = request.form.get('amount')
        
        if action == 'buy':
            if main.investment.buyBond(customer_name, bond_id, amount):
                return redirect(url_for("bank_views.investmentsPage", customer_name=customer_name))
            else:
                return render_template("/investments/bonds.html", customer_name=customer_name, 
                                    available_bonds=available_bonds, error="Failed to buy bond")
        elif action == 'sell':
            if main.investment.sellBond(customer_name, bond_id, amount):
                return redirect(url_for("bank_views.investmentsPage", customer_name=customer_name))
            else:
                return render_template("/investments/bonds.html", customer_name=customer_name, 
                                    available_bonds=available_bonds, error="Failed to sell bond")
    
    return render_template("/investments/bonds.html", customer_name=customer_name, available_bonds=available_bonds)

@bank_views.route("/investments/futures", methods=["GET", "POST"])
def futuresPage():
    args = request.args
    customer_name = args.get("customer_name")
    # Get available futures contracts for display
    cursor = main.db.cursor()
    cursor.execute("SELECT symbol, name, price, margin_req, expiry FROM futures_table;")
    available_futures = cursor.fetchall()
    
    # Get current positions
    cursor.execute("SELECT id, symbol, amount, position_type, margin FROM customer_futures WHERE customer_name = %s;", (customer_name,))
    current_positions = cursor.fetchall()
    cursor.close()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'open':
            futures_symbol = request.form.get('futures_symbol')
            amount = request.form.get('amount')
            position_type = request.form.get('position_type')
            
            if main.investment.tradeFutures(customer_name, futures_symbol, amount, position_type):
                return redirect(url_for("bank_views.investmentsPage", customer_name=customer_name))
            else:
                return render_template("/investments/futures.html", customer_name=customer_name, 
                                    available_futures=available_futures, current_positions=current_positions,
                                    error="Failed to open futures position")
        
        elif action == 'close':
            position_id = request.form.get('position_id')
            
            if main.investment.closeFuturesPosition(customer_name, position_id):
                return redirect(url_for("bank_views.investmentsPage", customer_name=customer_name))
            else:
                return render_template("/investments/futures.html", customer_name=customer_name, 
                                    available_futures=available_futures, current_positions=current_positions,
                                    error="Failed to close futures position")
    
    return render_template("/investments/futures.html", customer_name=customer_name, 
                        available_futures=available_futures, current_positions=current_positions)

@bank_views.route("/bonus", methods=["GET", "POST"]) #type: ignore
def bonusPage():
    args = request.args
    customer_name = args.get("customer_name")
    question_id = main.atm.getRandomQuestionId()
    return render_template("/atm/bonus.html", question_text = main.atm.getQuestionTextById(question_id), question_id = question_id, customer_name = customer_name)


@bank_views.route("/getBonus", methods=["GET", "POST"]) #type: ignore
def getBonusPage():
    args = request.args
    customer_name = args.get("customer_name")
    customer_id = main.atm.getCustomerId(customer_name)
    answer = args.get("answer")
    question_id = args.get("question_id")
    print("[BONUS] Checking")
    if main.atm.checkAnswer(answer, question_id) and main.atm.isAnswered(customer_id, question_id)==False:
        main.atm.setAnswered(customer_id, question_id)
        main.atm.rundeposit(customer_id, 100)
        print("[BONUS] Checking [GOOD]")

    return redirect(url_for("auth_views.accountPage", customer_name = customer_name))







"""from flask import Blueprint, render_template, request, jsonify, redirect, url_for

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
    return redirect(url_for("bank_views.atmPage", customer_name = customer_name))"""