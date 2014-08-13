# Create your views here.
from helper import get_query
from django.shortcuts import render
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from useraccounts.models import Customer

def search_result(request):
    """
    searches and displays the results for the query entered according 
    to the checkboxes selected
    """
    title = 'Search'
    results=[]
    result_fields = []
    selected_fields_client = request.GET.getlist('client_fields')
    selected_fields_order = request.GET.getlist('order')
    selected_fields_constraints = request.GET.getlist('additional_constraints')
    avail_list_dict_client = {'name':'user__username', 'city':'address__city',
                              'phone':'telephone','joining date':'date_joined',
                              'company':'company'}
    avail_list_dict_order = {'quantity':'qty','unit price':'item__price_per_unit',
                             'item':'item__name','discount':'purchase_order__total_discount','debit':
                             'purchase_order__is_debit', 'total price':'price'}
    avail_list = []
    avail_list2=[]
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']  
    amt_g = request.GET['amount_greater_than']
    amt_l = request.GET['amount_less_than']
    
    """
    For client Search
    """
    if 'Client' in request.GET:
        result_fields.append(selected_fields_client)
        search_fields = []
        for value in selected_fields_client:
            search_value = avail_list_dict_client[value]
            search_fields.append(search_value)

        query_string = ''
        found_entries = None
        if ('search' in request.GET) and request.GET['search'].strip():
            query_string = request.GET['search']
            entry_query = get_query(query_string, search_fields)
            found_entries = Customer.objects.filter(entry_query)
            for entries in found_entries:
                temp = []
                if 'date' in selected_fields_constraints:
                    for value in search_fields:
                        obj = Customer.objects.filter(id=entries.id,
                        date_joined__range=(start_date,end_date)).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                else:                    
                    for value in search_fields:
                        obj = Customer.objects.filter(id=entries.id).values(
                              value)
                        for temp_result in obj:
                            temp.append(temp_result)
                results.append(temp)
                
    """
    For Order Search
    """                
    if 'Order' in request.GET:
        result_fields.append(selected_fields_order)
        search_fields = []
        for value in selected_fields_order:
            search_value = avail_list_dict_order[value]
            search_fields.append(search_value)
        query_string = ''
        found_entries = ''
        search_fields.append('purchase_order__id')
        if ('search' in request.GET) and request.GET['search'].strip():
            query_string = request.GET['search']
            entry_query = get_query(query_string,search_fields)
            found_entries = PurchasedItem.objects.filter(entry_query)
            for entries in found_entries:
                temp=[]
                
                """
                if Debit, Date, 'Amount greater than'(gt), 
                'Amount lesser than'(lt) checkboxes are selected
                """
                if 'debit' in selected_fields_order and 'date' in selected_fields_constraints and 'gt' in selected_fields_constraints and 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(
                              id=entries.id,purchase_order__is_debit=1,
                              purchase_order__date_time__range=(start_date,
                              end_date), price__gt= amt_g, price__lt= 
                              amt_l).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if  Date, 'Amount greater than'(gt), 'Amount lesser than'
                (lt) checkboxes are selected
                """            
                if 'date' and 'gt' in selected_fields_constraints and 'lt' in selected_fields_constraints and not 'debit' in selected_fields_order:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__date_time__range=(start_date,
                              end_date),price__gt=amt_g, price__lt= 
                              amt_l).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if Debit, 'Amount greater than'(gt), 'Amount lesser than'
                (lt) checkboxes are selected
                """         
                if 'debit' in selected_fields_order and not 'date' in selected_fields_constraints and 'gt' in selected_fields_constraints and 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__is_debit = 1,price__gt=amt_g,
                              price__lt=amt_l).values(value)
                        for temp_result in obj:
                            temp.append(temp_result) 
                            
                """
                if Debit, Date, 'Amount lesser than'(lt) checkboxes are 
                selected
                """                                                           
                if 'debit' in selected_fields_order and 'date' in selected_fields_constraints  and 'lt' in selected_fields_constraints and not 'gt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__is_debit = 1, price__lt=
                              amt_l).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if Debit, Date, 'Amount greater than'(gt) checkboxes are 
                selected
                """            
                if 'debit' in selected_fields_order and 'date' in selected_fields_constraints and 'gt' in selected_fields_constraints and not 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__is_debit=1,
                              purchase_order__date_time__range=(start_date,
                              end_date), price__gt=amt_g).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if  'Amount greater than'(gt), 'Amount lesser than'(lt) 
                checkboxes are selected
                """            
                if not 'debit' in selected_fields_order and not 'date' in selected_fields_constraints and 'gt' in selected_fields_constraints and 'lt' in selected_fields_constraints:
                    for value in search_fields:

                        obj = PurchasedItem.objects.filter(id=entries.id,
                              price__gt=amt_g,price__lt=amt_l).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if Debit, 'Amount lesser than'(lt) checkboxes are 
                selected
                """            
                if 'debit' in selected_fields_order and not 'date' in selected_fields_constraints and not 'gt' in selected_fields_constraints and 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__is_debit = 1,price_lt= 
                              amt_l).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)  
                            
                """
                if Debit, 'Amount greater than'(gt), checkboxes are 
                selected
                """                                          
                if 'debit' in selected_fields_order and not 'date' in selected_fields_constraints and not 'lt' in selected_fields_constraints and 'gt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__is_debit = 1, price__gt=
                              amt_g).values(value)
                        for temp_result in obj:
                            temp.append(temp_result) 
                             
                """
                if  Date, 'Amount greater than'(gt) checkboxes are 
                selected
                """                                                           
                if not 'debit' in selected_fields_order and not 'lt' in selected_fields_constraints and 'date' in selected_fields_constraints and 'gt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__date_time__range=(start_date,
                              end_date),price__gt=amt_g).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if  Date, 'Amount lesser than'(lt) checkboxes are 
                selected
                """            
                if not 'debit' in selected_fields_order and not 'gt' in selected_fields_constraints and 'date' in selected_fields_constraints and 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__date_time__range=(start_date,
                              end_date), price__lt=amt_l).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if Debit, Date checkboxes are selected
                """            
                if 'debit' in selected_fields_order and 'date' in selected_fields_constraints and not 'gt' in selected_fields_constraints and not 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__is_debit = 1,
                              purchase_order__date_time__range=(start_date,
                              end_date)).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if Debit checkbox is selected
                """             
                if 'debit' in selected_fields_order and not 'date' in selected_fields_constraints and not 'gt' in selected_fields_constraints and not 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__is_debit = 1).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if Date checkbox is selected
                """            
                if not 'debit' in selected_fields_order and  'date' in selected_fields_constraints and  not 'gt' in selected_fields_constraints and not 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              purchase_order__date_time__range=(start_date,
                              end_date)).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                              
                """
                if  'Amount greater than'(gt) checkboxes is selected
                """                                                           
                if not 'debit' in selected_fields_order and 'gt' in selected_fields_constraints and not 'date' in selected_fields_constraints and not 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id, 
                              price__gt=amt_g).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                            
                """
                if 'Amount lesser than'(lt) checkbox is selected
                """            
                if not 'debit' in selected_fields_order and 'lt' in selected_fields_constraints and not 'date' in selected_fields_constraints and not 'gt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=entries.id,
                              price__lt=amt_l).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                """
                if none of the checkboxes - Debit, Date, 'Amount 
                greater than'(gt), 'Amount lesser than'(lt) are 
                selected
                """            
                if not 'debit' in selected_fields_order and not 'date' in selected_fields_constraints and not 'gt' in selected_fields_constraints and not 'lt' in selected_fields_constraints:
                    for value in search_fields:
                        obj = PurchasedItem.objects.filter(id=
                              entries.id).values(value)
                        for temp_result in obj:
                            temp.append(temp_result)
                results.append(temp)
                
    if 'search' in request.GET:
        title = request.GET['search']
    return render(request, 'reports/search_result.html', {'results':
                results,'title': title,'result_fields':result_fields,
                })



