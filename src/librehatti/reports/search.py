from django.shortcuts import render
from forms import ClientForm
from forms import OrderForm
from forms import AddConstraints
from django.http import HttpResponse

def search(request):
    """
    View to display "search.html" i.e. the search interface or form.
    
    First it'll check which type of request is i.e; 'search' request or 
    'generate register' request. On the basis of that, it'll assign code to 
    search_type_code which will be used in template.

    It'll raise an exception if anyone give invalid value in 'type'.
    """
    try:
        if request.GET['type'] == 'search':
            submit_url = '/search_result/'
            search_type_code = '1'
        elif request.GET['type'] == 'register':
            submit_url = '/generate_register/'
            search_type_code = '2'
        else:
    	    return HttpResponse('<h1>Page not found</h1>')
    except:
    	return HttpResponse('<h1>Invalid URL</h1>')

    client_form = ClientForm()
    order_form = OrderForm()
    add_constraints=  AddConstraints()
    temp = {'client_form':client_form,'order_form':order_form, 
            'add_constraints':add_constraints,'code':search_type_code,
            'url':submit_url}
    return render(request, 'reports/search.html',temp)
