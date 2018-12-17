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
    
    def productCreate(self, product_row):
        product_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'product.template', 'create', product_row)
        return product_id

    def productSearch(self, product_name):
        odoo_filter = [[("name", "=", product_name)]]
        product_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'product.template', 'search', odoo_filter)
        return product_id[0]

    def productRead(self, product_id):
        read_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'product.template', 'read', [product_id], {"fields": ["id","name","email"]})
        return read_result

    def productUpdate(self, product_id, odoo_filter):
        update_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'product.template', 'write', [product_id, odoo_filter])
        return update_result

    def productDelete(self, product_id):
        delete_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'product.template', 'unlink', [product_id])
        return delete_result

def main():
    od = Odoo()
    od.authenticateOdoo()

""" 
    #Copy each function outside the comment section to test independently

    # Create
    product_row = [{
        "name":"Redux", 
        "sale_ok":True, 
        "purchase_ok":False, 
        "can_be_expensed":False, 
        "type":"service", 
        "list_price":2500}]
    product_id = od.productCreate(product_row)
    print(product_id)

    #Search
    product_id = od.productSearch("Redux")
    print(product_id)

    #Read
    result = od.productRead(product_id)
    print(result)
 
    #Update
    odoo_filter = {"list_price":1500}
    result = od.productUpdate(product_id, odoo_filter)
    print(result)

    #Delete
    result = od.productDelete(product_id)
    print(result)
""" 

if __name__ == '__main__':
    main()