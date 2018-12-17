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
        self.ODOO_COMMON = xmlrpc.client.ServerProxy(self.URL_COMMON,allow_none=True)
        self.ODOO_OBJECT = xmlrpc.client.ServerProxy(self.URL_OBJECT,allow_none=True)
        self.UID = self.ODOO_COMMON.authenticate(self.DATA, self.USER, self.PASS, {})

    def paymentCreate(self,paymentCreate_args):
        payment_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'account.payment', 'create', paymentCreate_args)
        return payment_id
    
    def paymentConfirm(self,paymentConfirm_args):
        payment_confirm = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'account.payment', 'post', paymentConfirm_args)
        return payment_confirm

def main():
    od = Odoo()
    od.authenticateOdoo()

    #1 Create Payment
    paymentCreate_args = [{
        "amount": 7000
        ,"communication": False
        ,"currency_id": 153
        ,"destination_journal_id": False
        ,"journal_id": 8
        ,"message_attachment_count": 0
        ,"partner_bank_account_id": False
        ,"partner_id": 13
        ,"partner_type": "customer"
        ,"payment_date": "2018-12-03"
        ,"payment_method_id": 1
        ,"payment_type": "inbound"
        ,"x_cbc_transaction_id":"0123456789"
        ,"x_hyperpay_transaction_id":"0123456789"
        }]
    payment_id = od.paymentCreate(paymentCreate_args)
    print('payment_id = %s' % payment_id)

    #2 Confirm Payment
    confirm_payment = od.paymentConfirm([payment_id])
    if confirm_payment == True:
        print('payment confirmed')

if __name__ == '__main__':
    main()