class UserLogin():
    def fromDB(self, customer_id, db):
        self.__customer = db.getCustomer(customer_id)
        return self
    
    def create(self, customer):
        self.__customer = customer
        return self

    def isAuthenticated(self):
        return True

    def isActive(self):
        return True
    
    def isAnonymous(self):
        return False
    
    def getId(self):
        return str(self.__customer['id']) #str or int?