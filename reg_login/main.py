'''
Simple login
with mysql database
poor perfomance, but anyway its iobound
'''



'''
TODO: loan system
check when send money
'''
#import mysql driver and connect to database with (host, user, password and database name) info
import psycopg2


db = psycopg2.connect(database="postgres", user="postgres", password="admin", port=13337)
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
        "()",
        "or",
        "=",
        "==",
        "and"
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
    def login(customer_name, password) -> bool:
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
                return True
        except: pass
        return False


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
    
    def getCustomer(customer_id) -> str:
        '''
    Login command to take user input and check is it password.\n
    takes 2 args
        '''
        try:
            with db.cursor() as cursor:
                cursor.execute(f"select customer_id from customers_table where customer_name = '{customer_name.lower()}' and customer_password = '{password}';") # type: ignore
                result = cursor.fetchone()
                if not result:
                    return False
                return result
        except:
            print("[GET CUSTOMER ERROR]")
        return False
    