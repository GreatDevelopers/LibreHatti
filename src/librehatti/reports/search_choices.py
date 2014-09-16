CLIENT_FIELD_CHOICES = ( ('Name', 'Name'), ('City', 'Address'),
    ('Phone', 'Phone'),('Company', 'Company'),
    )

CLIENT_ORDER_CHOICES= ( ('Order Date', 'Order Date'),('Discount', 'Discount'), 
	('Debit', 'Debit'), ('Total Without Taxes', 'Total Amount without Taxes'),
	('TDS','TDS'),('Total With Taxes', 'Total Amount with Taxes')
    )

CONSTRAINT_CHOICES= ( ('date', 'Date'),('gt', 'Amount greater than'),
    ('lt', 'Amount lesser than'),
    )

MONTH_CHOICES = (('','------'),('1', 'January'),('2', 'February'),('3','March'),
    ('4', 'April'),('5', 'May'),('6','June'),('7', 'July'),('8', 'August'),
    ('9','September'),('10', 'October'),('11', 'November'),('12','December'),
)
