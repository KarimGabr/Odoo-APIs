import xmlrpc.client
import datetime

class Odoo():
    def __init__(self):
        self.DATA = "cbc_payments" # db name
        self.USER = "admin" # email address
        self.PASS = "admin" # password
        self.PORT = "8069" # port
        self.URL  = "http://127.0.0.1" # base url
        self.URL_COMMON = "{}:{}/xmlrpc/2/common".format(self.URL, self.PORT)
        self.URL_OBJECT = "{}:{}/xmlrpc/2/object".format(self.URL, self.PORT)
 
    def authenticateOdoo(self):
        self.ODOO_COMMON = xmlrpc.client.ServerProxy(self.URL_COMMON)
        self.ODOO_OBJECT = xmlrpc.client.ServerProxy(self.URL_OBJECT)
        self.UID = self.ODOO_COMMON.authenticate(self.DATA, self.USER, self.PASS, {})
    
    def contactCreate(self, contact_row):
        contact_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'res.partner', 'create', contact_row)
        return contact_id

    def contactSearch(self, contact_name):
        odoo_filter = [[("name", "=", contact_name)]]
        contact_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'res.partner', 'search', odoo_filter)
        return contact_id[0]

    def contactRead(self, contact_id):
        read_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'res.partner', 'read', [contact_id], {"fields": ["id","name","email"]})
        return read_result

    def contactUpdate(self, contact_id, odoo_filter):
        update_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'res.partner', 'write', [contact_id, odoo_filter])
        return update_result

    def contactDelete(self, contact_id):
        delete_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'res.partner', 'unlink', [contact_id])
        return delete_result

def main():
    od = Odoo()
    od.authenticateOdoo()

    

""" 
    #Copy each function outside the comment section to test independently

    #Create
    contact_row = [{"name":"Gabr","email":"gabr@gabr.com"}]
    contact_id = od.contactCreate(contact_row)
    print(contact_id)

	#Search
    contact_id = od.contactSearch("Gabr")
    print(contact_id)

    #Read
    result = od.contactRead(contact_id)
    print(result)
 
    #Update
    odoo_filter = {"website":"www.gabr.com", "street":"gabr street"}
    result = od.contactUpdate(contact_id, odoo_filter)
    print(result)

    #Delete
    result = od.contactDelete(contact_id)
    print(result)
"""

if __name__ == '__main__':
    main()