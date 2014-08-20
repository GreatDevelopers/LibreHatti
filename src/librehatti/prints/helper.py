#To convert digits into words
 
def num2eng(n):
    words = ''
    units = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 
             'Eight', 'Nine','Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen',
             'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['','Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy',
            'Eighty', 'Ninety']

    for group in ['', 'Hundred', 'Thousand', 'Lakh', 'Crore']:
        if group in ['', 'Thousand', 'Lakh']:
            n, digits = n // 100, n % 100
        elif group == 'Hundred':
            n, digits = n // 10, n % 10
        else:
            digits = n
    
        if digits in range (1, 20):
            words = units [digits] + ' ' + group + ' ' + words
        elif digits in range (20, 100):
            ten_digit, unit_digit = digits // 10, digits % 10
            words = tens [ten_digit] + ' ' + units [
                    unit_digit] + ' ' + group + ' ' + words
        elif digits >= 100:
            words = num2eng (digits) + ' crore ' + words
    return words
