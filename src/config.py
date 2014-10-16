"""useraccounts_Address"""

    _STREET_ADDRESS = 'Address'
    _PROVINCE = 'State'

"""useraccounts_HattiUser"""

    _USER = 'Buyer'
    _TELEPHONE = 'Phone'
    _DATE_JOINED = 'Joining_date'

"""useraccounts_AdminOrganisation"""

    _ORGANISATION_TYPE = 'org_type'
 
"""useraccounts_Customer"""

    _TITLE = 'Name'
    _COMPANY = 'Firm'

"""catalog_Product"""
 
    _PRICE_PER_UNIT = 'Item_Price'
    
"""catalog_PurchaseOrder"""

    _BUYER = 'Client' 
    _DELIVERY_ADDRESS = 'Address'
    _ORGANISATION = 'Firm'
    _MODE_OF_PAYMENT = 'Payment_mode'
   
"""catalog_Surcharge"""

    _TAX_NAME = 'tax'
    _TAX_EFFECTED_FROM = 'start_date'		
    _TAX_APPLIED_TILL = 'end_date'

"""catalog_PurchasedItem"""

    _PURCHASE_ORDER = 'Order'
    _ITEM = 'Test'
    _PRICE = 'Rate'

"""catalog_TaxesApplied"""

    _PURCHASE_ORDER = 'Order' 

"""catalog_Bill"""

    _PURCHASE_ORDER = 'Order' 
    _DELIVERY_CHARGES = 'extra_charges'

"""voucher_FinancialSession"""

    _SESSION_START_DATE = 'start_date'
    _SESSION_END_DATE = 'end_date'

"""voucher_Distribution"""

    _COLLEGE_INCOME = 'Income'
    _ADMIN_CHARGES = 'Charges'

"""voucher_VoucherId"""

    _PURCHASE_ORDER = 'Order_placed'
    _PURCHASED_ITEM = 'Item'

#voucher_CalculateDistribution //(TODO)

    

"""bills_QuotedOrder"""

    _BUYER_ID = 'id'
    _DELIVERY_ADDRESS = 'Address'
    _ORGANISATION = 'Firm'
    _mode_of_payment = 'Payment_mode'
    _IS_ACTIVE = 'Active/Inactive'
    _CONFIRM_STATUS = 'Status'

"""bills_QuotedItem"""

    _QUOTE_ORDER = 'Order'
    _PRICE = 'Rate'
    _ITEM = 'Test'


"""bills_QuoteTaxesApplied"""

    _QUOTE_ORDER = 'Order'

"""suspense_SuspenseOrder"""

    _PURCHASE_ORDER = 'Order'
    _DISTANCE_ESTIMATED = 'distance_covered'

"""suspense_SuspenseClearance"""

    _WORK_CHARGE = 'Charges'
    _CAR_TAXI_CHARGE = 'Transportation_charges'
    _TEST_DATE = 'Start_date'
    _CLEAR_DATE = 'End_date'

"""suspense_Department"""

    _TITLE = 'Name'
    _PHONE = 'Contact'
 
"""suspense_Staff"""

    _CODE = 'Id'
    _POSITION = 'Designation'

"""suspense_TaDa"""

    _TADA_AMOUNT = 'tada_charges'
    








   



    





