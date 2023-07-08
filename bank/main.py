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

def updateCache(customer_id, cash_amount):
        with redis.Redis("localhost", 6379) as redis_client:
            redis_client.set(customer_id, cash_amount)
            print(f"[SET]: {customer_id}: {cash_amount}")


class atm():
    def __init__(self) -> None:
        pass

    

    def rundeposit(customer_id, cash) -> bool:
        '''
    'Deposit command to update CASH at customer_id.\n
    Cash += cash_input for user.\n
    takes 0 args, only asks inside of function.
    '''
        cursor = db.cursor()
        
        try:
            if int(cash) >= 0:
                print("Depositing cash")
                cursor.execute(f"update customers_table set customer_cash = customer_cash + {cash} where customer_id = '{customer_id}';")

                cursor.execute(f"select customer_cash from customers_table where customer_id = '{customer_id}';")
                updateCache(customer_id, cursor.fetchone()[0])

                cursor.close()
                db.commit()
                return True
        except Exception as err: print(err)
        return False


    def runwithdraw(customer_id, cash) -> bool:
        '''
    Withdraw command to update CASH at customer_id.\n
    Cash -= cash_input for user.\n
    takes 0 args, only asks inside of function.
    '''
        cursor = db.cursor()
        try:
            if int(cash) >= 0:
                cursor.execute(f"update customers_table set customer_cash = customer_cash - {cash} where customer_id = '{customer_id}';")

                cursor.execute(f"select customer_cash from customers_table where customer_id = '{customer_id}';")
                updateCache(customer_id, cursor.fetchone()[0])

                cursor.close()
                db.commit()
                return True
        except: pass
        return False


    def runsend(customer_id, cash, taker) -> bool:
        '''
    Send command to update CASH at customer_id[i] and customer_id[j].\n
    Sends cash from one user to another.\n
    takes 0 args, only asks inside of function.
    '''
        cursor = db.cursor()

        try: #check how much money customer do have
            print("Checking cash")
            cursor.execute(f"select customer_cash from customers_table where customer_id = '{customer_id}';")
            cash_on_sender_card = cursor.fetchone()[0]
            print(cash_on_sender_card)
        except: return False


        try:
            cash = int(cash)
            cash_on_sender_card = int(cash_on_sender_card)

            if cash >= 0 and cash_on_sender_card - cash >= 0:
                print("Sending cash")
                cursor.execute(f"update customers_table set customer_cash = customer_cash + {cash} where customer_id = '{taker}';")
                print("send #1")
                cursor.execute(f"update customers_table set customer_cash = customer_cash - {cash} where customer_id = '{customer_id}';")
                print("send #2")

                cursor.execute(f"select customer_cash from customers_table where customer_id = '{customer_id}';")
                updateCache(customer_id, cursor.fetchone()[0])

                cursor.execute(f"select customer_cash from customers_table where customer_id = '{taker}';")
                updateCache(customer_id, cursor.fetchone()[0])

                cursor.close()
                db.commit()
                return True
        except: pass
        return False
    

    def getCashAmount(customer_id):
        cursor = db.cursor()
        redis_client = redis.Redis("localhost", 6379)

        moneyFromcache = redis_client.get(customer_id)

        if moneyFromcache is None:
            print("set into cache")
            cursor.execute(f"select customer_cash from customers_table where customer_id = '{customer_id}';")
            customer_cash = cursor.fetchone()
            redis_client.set(customer_id, customer_cash[0])

        elif moneyFromcache is not None:
            print("from cache", moneyFromcache)
            return int(moneyFromcache)

        try:
            print("get from db")
            cursor.execute(f"select customer_cash from customers_table where customer_id = '{customer_id}';")
            customer_cash = cursor.fetchone()
            cursor.close()
            return customer_cash[0]
        except: pass


    
    def getCustomerId(customer_name) -> int:

        cursor = db.cursor()

        cursor.execute(f"select customer_id from customers_table where customer_name = '{customer_name.lower()}';") # type: ignore
        result = cursor.fetchone()

        if isinstance(result[0], int):
            return result[0]
        return 0



