'''
Simple console-based ATM programm
with mysql database
poor perfomance, but anyway its iobound
'''



'''
TODO: loan system
check when send money
'''
#import mysql driver and connect to database with (host, user, password and database name) info
import psycopg2
import redis


db = psycopg2.connect(database="db", user="postgres", password="admin", port=13337)
cursor = db.cursor()
print("Connected successfully")


def securityCheck(*args) -> bool:
    '''
    Checks user input for: blacklisted words, going out-of-bounds
\n
    returns bool, True = blacklisted words are in input, False = not
    '''
    violated = False
    blacklisted_words = [
        "select",
        "drop",
        "delete",
        "where",
        "insert",
        "commit",
        "rollback",
        ";"
        "from",
        "*",
        "update",
        "()"
                         ]
    
    for word in args:
        if len(word) > 20: 
            violated = True

        if word.lower() in blacklisted_words:
            violated = True

    if violated:
        return True
    return False


class accountManagment:
    def login(customer_name, password) -> str:
        '''
    Login command to take user input and check is it password.\n
    takes 2 args
        '''
        cursor = db.cursor()

        cursor.execute(f"select customer_id from customers_table where customer_name = '{customer_name.lower()}' and customer_password = '{password}';") # type: ignore
        result = cursor.fetchone()
        cursor.close()
        try:
            if isinstance(result[0], int) and securityCheck(customer_name, password)==False:
                return customer_name
        except: pass
        return "no_customer"


    def changePassword(customer_name, old_password, new_password) -> bool:
        '''
    ChngPass command to take user input and set it as password.\n
    takes 3 args.
        '''
        cursor = db.cursor()

        cursor.execute(f"select customer_id from customers_table where customer_name = '{customer_name.lower()}' and customer_password = '{old_password}';") # type: ignore
        result = cursor.fetchone()

        try: 
            if isinstance(result[0], int) and securityCheck(customer_name, old_password, new_password)==False:
                cursor.execute(f"update customers_table set customer_password = '{new_password}' where customer_name = '{customer_name}';")
                cursor.close()
                db.commit()
                return True 
        except: pass
        return False


    def register(customer_name, password) -> bool:
        '''
    Register command to take user input and load it into customers_table.\n
    takes 2 args, True = success, False = not.
        '''
        cursor = db.cursor()
        try: 
            if securityCheck(customer_name, password)==False:
                cursor.execute(f"insert into customers_table(customer_name, customer_password) values ('{customer_name}', '{password}');")
                cursor.close()
                db.commit()
                return True
        except: pass
        return False

        
    def deleteAcc(customer_name, password) -> bool:
        '''
    Delete command to delete a row with specified id \n
    takes 2 args, True = success , False = not.
        '''

        cursor = db.cursor()
        try: 
            if securityCheck(customer_name, password)==False:
                cursor.execute(f"delete from customers_table where customer_name = '{customer_name}' and customer_password = '{password}';")
                cursor.close()
                db.commit()
                return True
        except: pass
        return False


class atm():
    def deposit(customer_name, cash) -> bool:
        '''
    'Deposit command to update CASH at customer_id.\n
    Cash += cash_input for user.\n
    takes 0 args, only asks inside of function.
    '''
        cursor = db.cursor()
        try:
            if int(cash) >= 0 and securityCheck(customer_name)==False:
                print("Depositing cash")
                cursor.execute(f"update customers_table set customer_cash = customer_cash + {cash} where customer_name = '{customer_name}';")
                cursor.close()
                db.commit()
                return True
        except: pass
        return False


    def withdraw(customer_name, cash) -> bool:
        '''
    Withdraw command to update CASH at customer_id.\n
    Cash -= cash_input for user.\n
    takes 0 args, only asks inside of function.
    '''
        cursor = db.cursor()
        try:
            if int(cash) >= 0 and securityCheck(customer_name)==False:
                cursor.execute(f"update customers_table set customer_cash = customer_cash - {cash} where customer_name = '{customer_name}';")
                cursor.close()
                db.commit()
                return True
        except: pass
        return False


    def send(customer_name, cash, taker) -> bool:
        '''
    Send command to update CASH at customer_id[i] and customer_id[j].\n
    Sends cash from one user to another.\n
    takes 0 args, only asks inside of function.
    '''
        cursor = db.cursor()

        try: #check how much money customer do have
            print("Checking cash")
            cursor.execute(f"select customer_cash from customers_table where customer_name = '{customer_name}';")
            cash_on_sender_card = cursor.fetchone()[0]
            print(cash_on_sender_card)
        except: return False


        try:
            cash = int(cash)
            cash_on_sender_card = int(cash_on_sender_card)

            if cash >= 0 and cash_on_sender_card - cash >= 0 and securityCheck(customer_name, taker)==False:
                print("Sending cash")
                cursor.execute(f"update customers_table set customer_cash = customer_cash + {cash} where customer_name = '{taker}';")
                print("send #1")
                cursor.execute(f"update customers_table set customer_cash = customer_cash - {cash} where customer_name = '{customer_name}';")
                print("send #2")
                cursor.close()
                db.commit()
                return True
        except: pass
        return False
    

    def getCashAmount(customer_name):
        cursor = db.cursor()
        redis_client = redis.Redis("localhost", 6379)

        moneyFromcache = redis_client.get(customer_name)

        if moneyFromcache is None:
            print("set into cache")
            cursor.execute(f"select customer_cash from customers_table where customer_name = '{customer_name}';")
            customer_cash = cursor.fetchone()
            redis_client.set(customer_name, customer_cash[0])

        elif moneyFromcache is not None:
            print("from cache", moneyFromcache)
            return int(moneyFromcache)

        try:
            print("get from db")
            cursor.execute(f"select customer_cash from customers_table where customer_name = '{customer_name}';")
            customer_cash = cursor.fetchone()
            cursor.close()
            return customer_cash[0]
        except: pass


class investment:
    def buyStock(customer_name, stock_symbol, amount) -> bool:
        '''
    Buy stock for a customer.
    Parameters:
    - customer_name: name of the customer
    - stock_symbol: stock ticker symbol
    - amount: number of shares to buy
    Returns: True if successful, False otherwise
        '''
        cursor = db.cursor()
        try:
            # Get current stock price (in real app would fetch from API)
            cursor.execute(f"select price from stocks_table where symbol = '{stock_symbol}';")
            stock_price = cursor.fetchone()[0]
            total_cost = float(stock_price) * int(amount)
            
            # Check if customer has enough cash
            cursor.execute(f"select customer_cash from customers_table where customer_name = '{customer_name}';")
            cash = cursor.fetchone()[0]
            
            if float(cash) >= total_cost and securityCheck(customer_name, stock_symbol)==False:
                # Deduct cash
                cursor.execute(f"update customers_table set customer_cash = customer_cash - {total_cost} where customer_name = '{customer_name}';")
                
                # Add to customer's portfolio
                cursor.execute(f"select * from customer_investments where customer_name = '{customer_name}' and symbol = '{stock_symbol}' and type = 'stock';")
                exists = cursor.fetchone()
                
                if exists:
                    cursor.execute(f"update customer_investments set amount = amount + {amount} where customer_name = '{customer_name}' and symbol = '{stock_symbol}' and type = 'stock';")
                else:
                    cursor.execute(f"insert into customer_investments(customer_name, symbol, type, amount) values ('{customer_name}', '{stock_symbol}', 'stock', {amount});")
                
                cursor.close()
                db.commit()
                return True
        except: pass
        return False
    
    def sellStock(customer_name, stock_symbol, amount) -> bool:
        '''
    Sell stock for a customer.
    Parameters:
    - customer_name: name of the customer
    - stock_symbol: stock ticker symbol
    - amount: number of shares to sell
    Returns: True if successful, False otherwise
        '''
        cursor = db.cursor()
        try:
            # Check if customer has enough shares
            cursor.execute(f"select amount from customer_investments where customer_name = '{customer_name}' and symbol = '{stock_symbol}' and type = 'stock';")
            owned_amount = cursor.fetchone()[0]
            
            if int(owned_amount) >= int(amount) and securityCheck(customer_name, stock_symbol)==False:
                # Get current stock price
                cursor.execute(f"select price from stocks_table where symbol = '{stock_symbol}';")
                stock_price = cursor.fetchone()[0]
                total_value = float(stock_price) * int(amount)
                
                # Add cash to customer account
                cursor.execute(f"update customers_table set customer_cash = customer_cash + {total_value} where customer_name = '{customer_name}';")
                
                # Update portfolio
                if int(owned_amount) == int(amount):
                    cursor.execute(f"delete from customer_investments where customer_name = '{customer_name}' and symbol = '{stock_symbol}' and type = 'stock';")
                else:
                    cursor.execute(f"update customer_investments set amount = amount - {amount} where customer_name = '{customer_name}' and symbol = '{stock_symbol}' and type = 'stock';")
                
                cursor.close()
                db.commit()
                return True
        except: pass
        return False
    
    def buyBond(customer_name, bond_id, amount) -> bool:
        '''
    Buy bond for a customer.
    Parameters:
    - customer_name: name of the customer
    - bond_id: bond identifier
    - amount: amount to invest in the bond
    Returns: True if successful, False otherwise
        '''
        cursor = db.cursor()
        try:
            # Get bond details
            cursor.execute(f"select price, yield from bonds_table where bond_id = '{bond_id}';")
            bond_details = cursor.fetchone()
            bond_price = bond_details[0]
            
            # Check if customer has enough cash
            cursor.execute(f"select customer_cash from customers_table where customer_name = '{customer_name}';")
            cash = cursor.fetchone()[0]
            
            if float(cash) >= float(amount) and securityCheck(customer_name, bond_id)==False:
                # Deduct cash
                cursor.execute(f"update customers_table set customer_cash = customer_cash - {amount} where customer_name = '{customer_name}';")
                
                # Add to customer's portfolio
                cursor.execute(f"select * from customer_investments where customer_name = '{customer_name}' and symbol = '{bond_id}' and type = 'bond';")
                exists = cursor.fetchone()
                
                if exists:
                    cursor.execute(f"update customer_investments set amount = amount + {amount} where customer_name = '{customer_name}' and symbol = '{bond_id}' and type = 'bond';")
                else:
                    cursor.execute(f"insert into customer_investments(customer_name, symbol, type, amount) values ('{customer_name}', '{bond_id}', 'bond', {amount});")
                
                cursor.close()
                db.commit()
                return True
        except: pass
        return False

    def sellBond(customer_name, bond_id, amount) -> bool:
        '''
    Sell bond for a customer.
    Parameters:
    - customer_name: name of the customer
    - bond_id: bond identifier
    - amount: amount of bond to sell
    Returns: True if successful, False otherwise
        '''
        cursor = db.cursor()
        try:
            # Check if customer owns this bond
            cursor.execute(f"select amount from customer_investments where customer_name = '{customer_name}' and symbol = '{bond_id}' and type = 'bond';")
            owned_amount = cursor.fetchone()[0]
            
            if float(owned_amount) >= float(amount) and securityCheck(customer_name, bond_id)==False:
                # Add cash to customer account (could include interest/penalties for early redemption)
                cursor.execute(f"update customers_table set customer_cash = customer_cash + {amount} where customer_name = '{customer_name}';")
                
                # Update portfolio
                if float(owned_amount) == float(amount):
                    cursor.execute(f"delete from customer_investments where customer_name = '{customer_name}' and symbol = '{bond_id}' and type = 'bond';")
                else:
                    cursor.execute(f"update customer_investments set amount = amount - {amount} where customer_name = '{customer_name}' and symbol = '{bond_id}' and type = 'bond';")
                
                cursor.close()
                db.commit()
                return True
        except: pass
        return False

    def tradeFutures(customer_name, futures_symbol, amount, position_type) -> bool:
        '''
    Trade futures contracts for a customer.
    Parameters:
    - customer_name: name of the customer
    - futures_symbol: futures contract symbol
    - amount: number of contracts
    - position_type: 'long' or 'short'
    Returns: True if successful, False otherwise
        '''
        cursor = db.cursor()
        try:
            # Get contract details
            cursor.execute(f"select price, margin_req from futures_table where symbol = '{futures_symbol}';")
            futures_details = cursor.fetchone()
            contract_price = futures_details[0]
            margin_requirement = futures_details[1]
            
            required_margin = float(contract_price) * int(amount) * float(margin_requirement)
            
            # Check if customer has enough cash for margin
            cursor.execute(f"select customer_cash from customers_table where customer_name = '{customer_name}';")
            cash = cursor.fetchone()[0]
            
            if float(cash) >= required_margin and securityCheck(customer_name, futures_symbol, position_type)==False:
                # Set aside margin
                cursor.execute(f"update customers_table set customer_cash = customer_cash - {required_margin} where customer_name = '{customer_name}';")
                
                # Record the futures position
                cursor.execute(f"insert into customer_futures(customer_name, symbol, amount, position_type, margin) values ('{customer_name}', '{futures_symbol}', {amount}, '{position_type}', {required_margin});")
                
                cursor.close()
                db.commit()
                return True
        except: pass
        return False

    def closeFuturesPosition(customer_name, position_id) -> bool:
        '''
    Close a futures position.
    Parameters:
    - customer_name: name of the customer
    - position_id: ID of the futures position
    Returns: True if successful, False otherwise
        '''
        cursor = db.cursor()
        try:
            # Get position details
            cursor.execute(f"select margin, symbol, amount, position_type from customer_futures where id = {position_id} and customer_name = '{customer_name}';")
            position = cursor.fetchone()
            margin = position[0]
            symbol = position[1]
            amount = position[2]
            position_type = position[3]
            
            if position and securityCheck(customer_name)==False:
                # Get current price
                cursor.execute(f"select price from futures_table where symbol = '{symbol}';")
                current_price = cursor.fetchone()[0]
                
                # Calculate profit/loss (simplified)
                initial_price_query = f"select open_price from customer_futures where id = {position_id};"
                cursor.execute(initial_price_query)
                initial_price = cursor.fetchone()[0]
                
                if position_type == 'long':
                    pnl = (float(current_price) - float(initial_price)) * int(amount)
                else:  # short
                    pnl = (float(initial_price) - float(current_price)) * int(amount)
                
                # Return margin + profit or - loss
                cursor.execute(f"update customers_table set customer_cash = customer_cash + {margin + pnl} where customer_name = '{customer_name}';")
                
                # Remove position
                cursor.execute(f"delete from customer_futures where id = {position_id};")
                
                cursor.close()
                db.commit()
                return True
        except: pass
        return False

    def getPortfolio(customer_name):
        '''
    Get a customer's investment portfolio.
    Parameters:
    - customer_name: name of the customer
    Returns: Dictionary with portfolio information
        '''
        cursor = db.cursor()
        portfolio = {'stocks': [], 'bonds': [], 'futures': []}
        
        try:
            # Get stocks
            cursor.execute(f"select symbol, amount from customer_investments where customer_name = '{customer_name}' and type = 'stock';")
            stocks = cursor.fetchall()
            for stock in stocks:
                cursor.execute(f"select price from stocks_table where symbol = '{stock[0]}';")
                price = cursor.fetchone()[0]
                portfolio['stocks'].append({
                    'symbol': stock[0],
                    'shares': stock[1],
                    'current_price': price,
                    'value': float(price) * int(stock[1])
                })
            
            # Get bonds
            cursor.execute(f"select symbol, amount from customer_investments where customer_name = '{customer_name}' and type = 'bond';")
            bonds = cursor.fetchall()
            for bond in bonds:
                portfolio['bonds'].append({
                    'bond_id': bond[0],
                    'amount': bond[1]
                })
            
            # Get futures
            cursor.execute(f"select id, symbol, amount, position_type, margin from customer_futures where customer_name = '{customer_name}';")
            futures = cursor.fetchall()
            for future in futures:
                portfolio['futures'].append({
                    'position_id': future[0],
                    'symbol': future[1],
                    'contracts': future[2],
                    'position': future[3],
                    'margin': future[4]
                })
            
            cursor.close()
            return portfolio
        except:
            if cursor:
                cursor.close()
            return portfolio



