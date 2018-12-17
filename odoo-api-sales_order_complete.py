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
    
    def quotationCreate(self, quotation_row):
        quotation_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'sale.order', 'create', quotation_row)
        return quotation_id

    def orderlineAdd(self, orderline_row):
        orderline_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'sale.order.line', 'create', orderline_row)
        return orderline_id

    def quotationConfirm(self, quotation_id):
        confirm_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'sale.order', 'action_confirm', [quotation_id])
        return confirm_result
    
    def deliveryCreate(self, delivery_row):
        delivery_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'stock.picking', 'create', delivery_row)
        return delivery_id

    def stockmoveCreate(self, stockmove_row):
        stockmove_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'stock.move', 'create', stockmove_row)
        return stockmove_id

    def deliveryConfirm(self, delivery_id):
        confirm_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'stock.picking', 'action_confirm', [delivery_id])
        return confirm_result

    def deliveryCheckAvailability(self, delivery_id):
        confirm_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'stock.picking', 'action_assign', [delivery_id])
        return confirm_result

    def deliveryValidate(self, delivery_id):
        confirm_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'stock.picking', 'button_validate', [delivery_id])
        return confirm_result

    def invoiceCreate(self, invoice_row):
        invoice_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'account.invoice', 'create', invoice_row)
        return invoice_id
    
    def invoicelineAdd(self, invoiceline_row):
        invoiceline_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'account.invoice.line', 'create', invoiceline_row)
        return invoiceline_id

    def invoiceValidate(self, invoice_id):
        confirm_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'account.invoice', 'action_invoice_open', [invoice_id])
        return confirm_result

    def paymentCreate(self, payment_row):
        payment_id = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'account.payment', 'create', payment_row)
        return payment_id

    def invoiceRegisterPayment(self,register_payment_row):
        confirm_result = self.ODOO_OBJECT.execute_kw(self.DATA, self.UID, self.PASS, 'account.payment', 'action_validate_invoice_payment', register_payment_row)
        return confirm_result

def main():
    od = Odoo()
    od.authenticateOdoo()

    #1 Create Quotation
    quotation_row = [{"partner_id":1,"payment_term_id":1}]
    quotation_id = od.quotationCreate(quotation_row)
    print('quotation_id = %s' % quotation_id)

    #2 Add Order line
    orderline_row = [{
		"product_id":9,
		"customer_lead":1,
		"product_uom_quantity":1,
		"product_uom":1,
        "qty_delivered":1,
		"order_id":quotation_id}]
    orderline_id = od.orderlineAdd(orderline_row)
    print('orderline_id = %s' % orderline_id)

    #3 Confirm Quotation
    result = od.quotationConfirm(quotation_id)
    print('quotation_confirmed = %s' % result)

    #4 Create Delivery Order
    delivery_row = [{
        "partner_id":1,
        "origin":"SO058",
        "location_id":1,
        "location_dest_id":1,
        "picking_type_id":2,}]
    delivery_id = od.deliveryCreate(delivery_row)
    print('delivery_order_id = %s' % delivery_id)

    #5 Add Stock Move
    stockmove_row = [{
        "company_id":1,
        "date":"2018-12-03 12:14:52",
        "date_expected":"2018-12-03 12:14:52",
        "location_id":1,
        "location_dest_id":1,
        "product_id":9,
        "product_uom_qty":1,
        "product_uom_id":1,
        "product_uom":1,
        "reserved_availability":1.0,
        "quantity_done":1.0,
        "name":"course",
        "picking_id":delivery_id}]
    stockmove_id = od.stockmoveCreate(stockmove_row)
    print('stockmove_id = %s' % stockmove_id)

    #6.1 Confirm Delivery Order(Odoo12)
    result = od.deliveryConfirm(delivery_id)
    print('delivery_confirmed = %s' % result)
    
    #6.2 Check Availablty for Delivery Order(Odoo12)
    result = od.deliveryCheckAvailability(delivery_id)
    print('delivery_availabilty = %s' % result)
    
    #6.3 Validate Delivery Order
    result = od.deliveryValidate(delivery_id)
    print('delivery_validated = %s' % result)

    #7 Create Invoice
    invoice_row = [{
        "partner_id":1,
        "payment_term_id":1,
        "origin":"lmao"}]
    invoice_id = od.invoiceCreate(invoice_row)
    print('invoice_id = %s' % invoice_id)

    #8 Add Invoice Line
    invoiceline_row = [{
        "product_id":9,
        "name":"lmao",
        "price_unit":12345, 
        "quantity":1,
        "invoice_id":invoice_id,
        "account_id":15
    }]
    invoiceline_id = od.invoicelineAdd(invoiceline_row)
    print('invoiceline_id = %s' % invoiceline_id)

    #9 Validate Invoice
    result = od.invoiceValidate(invoice_id)
    print('invoice_validated = %s' % result)

    #10 Create Payment
    payment_row = [{
        "amount":333.00,
        "communication":"INV/2018/0006/06",
        "currency_id":153,
        "journal_id":8,
        "partner_type": "customer",
        "payment_date":"2018-11-29",
        "payment_difference_handling":"open",
        "payment_method_id":1,
        "payment_token_id":False,
        "payment_type":"inbound",
        "writeoff_account_id":False,
        "writeoff_label":"Write-Off"

    }]
    payment_id = od.paymentCreate(payment_row)
    print('payment_id = %s' % payment_id)

    #11 Register Payment linked to Invoice
    register_payment_row = [
        [payment_id],
        {
            "active_id":invoice_id,
            "active_ids":[invoice_id],
            "active_model": "account.invoice",
            "default_invoice_ids":[[4,invoice_id,None]],
            "journal_type":"sale",
            "lang":"en_US",
            "search_disable_custom_filters": True,
            "type": "out_invoice",
            "tz": False,
            "uid": 2
        }
    ]

    print(register_payment_row)
    result = od.invoiceRegisterPayment(register_payment_row)
    print('invoice_payment_registered = %s' % result)

if __name__ == '__main__':
    main()