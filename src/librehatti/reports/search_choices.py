"""
It includes the choices used in forms.
"""

CLIENT_FIELD_CHOICES = (
    ("First Name", "First Name"),
    ("Last Name", "Last Name"),
    ("Title", "Title"),
    ("Street Address", "Street Address"),
    ("district", "district"),
    ("Phone", "Phone"),
    ("Company", "Company"),
)


CLIENT_ORDER_CHOICES = (
    ("Order Date", "Order Date"),
    ("Discount", "Discount"),
    ("Debit", "Debit"),
    ("Total Without Taxes", "Total Amount without Taxes"),
    ("Total With Taxes", "Total Amount with Taxes"),
)


CONSTRAINT_CHOICES = (
    ("date", "Date"),
    ("gt", "Amount greater than"),
    ("lt", "Amount lesser than"),
)


MONTH_CHOICES = (
    ("", "------"),
    ("1", "January"),
    ("2", "February"),
    ("3", "March"),
    ("4", "April"),
    ("5", "May"),
    ("6", "June"),
    ("7", "July"),
    ("8", "August"),
    ("9", "September"),
    ("10", "October"),
    ("11", "November"),
    ("12", "December"),
)
