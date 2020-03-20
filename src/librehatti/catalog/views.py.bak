from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render

from django.db.models import Sum, Max

from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.models import *
from librehatti.catalog.forms import AddCategory
from librehatti.catalog.forms import ItemSelectForm
from librehatti.catalog.forms import ChangeRequestForm
from librehatti.catalog.forms import ProductListForm
from librehatti.catalog.models import HeaderFooter
from librehatti.catalog.request_change import request_notify

from librehatti.prints.helper import num2eng

from librehatti.suspense.models import SuspenseOrder

from librehatti.voucher.models import VoucherId
from librehatti.voucher.models import CalculateDistribution
from librehatti.voucher.models import CategoryDistributionType
from librehatti.voucher.models import FinancialSession

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.db.models import Q

import simplejson

from django import forms

@login_required
def index(request):
    """
    It lists all the products and the user can select any product
    and can add them to the cart.
    Argument: Http Request
    Return: Render index.html
    """
    """error = {}
    categorylist = Category.objects.all()

    if categorylist.count() == 0:
        nocategory = True
        return render(request, 'catalog.html', {'nocategory': nocategory})
    productlist = Product.objects.all();

    if productlist.count() == 0:
        noproduct = True
        return render(request, 'catalog.html', {'noproduct': noproduct})

    return render(request,'catalog.html', {'productlist': productlist,
               'categorylist': categorylist})

    pass"""
    request_status = request_notify()
    return render(request,'index.html',{'request':request_status})



@login_required
def select_sub_category(request):
    """
    This view allows filtering of sub category according to parent
    category of item.
    Argument: Http Request
    Return: Filtered sub categories
    """
    parent_category = request.GET['cat_id']
    sub_categories = Category.objects.filter(parent=parent_category)
    sub_category_dict = {}
    for sub_category in sub_categories:
        sub_category_dict[sub_category.id] = sub_category.name
    return HttpResponse(simplejson.dumps(sub_category_dict))


def jsreverse(request):
    """
    This function reverse looks up the urls for the AJAX Requests
    Argument: Http Request
    Return: Dynamic Url
    """
    string_to_reverse = request.GET['string'];
    return HttpResponse(reverse(string_to_reverse))



@login_required
def select_item(request):
    """
    This view allows filtering of item according to sub category of item.
    Argument: Http Request
    Return: Filtered Products
    """
    cat_id = request.GET['cat_id']
    try:
        distrubtion = CategoryDistributionType.objects.get(category_id = cat_id)
        products = Product.objects.filter(category = cat_id)
        product_dict = {}
        for product in products:
            product_dict[product.id] = product.name
        return HttpResponse(simplejson.dumps(product_dict))
    except:
        return HttpResponse('0')


@login_required
def select_type(request):
    """
    This view allows filtering labs according to selected work.
    Argument: Http Request
    Return: Filtered Labs
    """
    type_id = request.GET['type_id']
    if type_id == '1':
        categories = Category.objects.filter(Q(name__icontains='Lab Work'))
    elif type_id == '2':
        categories = Category.objects.filter(Q(name__icontains='Field Work'))
    else:
        categories = Category.objects.filter(parent__name='Other Services')
    category_dict = {}
    for category in categories:
        category_dict[category.id] = category.name.split(':')[0]
    return HttpResponse(simplejson.dumps(category_dict))         


@login_required
def bill_cal(request):
    """
    This view calculate taxes on purchased order, bill data
    and save those values in database.
    Argument: Http Request
    Return: Redirect to Order Success Page
    """
    old_post = request.session.get('old_post')
    purchase_order_id = request.session.get('purchase_order_id')
    generate_tax = 1
    first_item = PurchasedItem.objects.values('item__category__id').\
    filter(purchase_order=purchase_order_id)[0]
    category_check = SpecialCategories.objects.filter(category=
        first_item['item__category__id'])
    if category_check:
        specialcategories = SpecialCategories.objects.values('tax').\
        filter(category=first_item['item__category__id'])[0]
        if specialcategories['tax'] == False:
            generate_tax = 0
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    purchase_order_obj = PurchaseOrder.objects.values('total_discount','tds').\
    get(id=purchase_order_id)
    purchase_item = PurchasedItem.objects.\
    filter(purchase_order=purchase_order_id).aggregate(Sum('price'))
    total = purchase_item['price__sum']
    price_total = total - purchase_order_obj['total_discount']
    totalplusdelivery = price_total
    surcharge = Surcharge.objects.values('id','value','taxes_included','tax_name')
    delivery_rate = Surcharge.objects.values('value').\
    filter(tax_name = 'Transportation')
    distance = SuspenseOrder.objects.filter\
    (purchase_order = purchase_order_id).aggregate(Sum('distance_estimated'))
    if distance['distance_estimated__sum']:
        delivery_charges = int(distance['distance_estimated__sum'])*\
            delivery_rate[0]['value']
        totalplusdelivery = price_total + delivery_charges

    else:
        delivery_charges = 0

    for value in surcharge:
        surcharge_id = value['id']
        surcharge_val = value['value']
        surcharge_tax = value['taxes_included']
        if surcharge_tax == 1 and generate_tax == 1:
            taxes = round((totalplusdelivery * surcharge_val)/100)
            surcharge_obj = Surcharge.objects.get(id=surcharge_id)
            taxes_applied_var = TaxesApplied.objects.filter(
                purchase_order = purchase_order, surcharge = surcharge_obj,
                tax = taxes, surcharge_name = value['tax_name'],
                surcharge_value = value['value'])
            if taxes_applied_var:
                pass
            else:
                taxes_applied = TaxesApplied(purchase_order = purchase_order,
                surcharge = surcharge_obj, tax = taxes, surcharge_name = value['tax_name'],
                surcharge_value = value['value'])
                taxes_applied.save()
    taxes_applied_temp = TaxesApplied.objects.\
    filter(purchase_order=purchase_order_id)
    if taxes_applied_temp:
        taxes_applied_obj = TaxesApplied.objects.\
        filter(purchase_order=purchase_order_id).aggregate(Sum('tax'))
        tax_total = taxes_applied_obj['tax__sum']
    else:
        tax_total = 0
    grand_total = price_total + tax_total + delivery_charges
    amount_received = grand_total - purchase_order_obj['tds']
    bill_obj = Bill.objects.filter(purchase_order=purchase_order)
    if bill_obj:
        pass
    else:
        bill = Bill(purchase_order = purchase_order, total_cost = price_total,
        total_tax = tax_total, grand_total = grand_total,
        delivery_charges = delivery_charges, amount_received = amount_received,
        totalplusdelivery=totalplusdelivery)
        bill.save()
    request.session['old_post'] = old_post
    request.session['purchase_order_id'] = purchase_order_id
    return HttpResponseRedirect(reverse\
        ("catalog:order_added_success"))


@login_required
def list_products(request):
    """
    This view lists products for viewing purpose
    Argument: Http Request
    Return: Render catalog page
    """ 
    if request.method == 'POST':
        form = ProductListForm(request.POST)
        if form.is_valid():
            select_lab = request.POST['select_lab']
            root_name = Category.objects.get(id=select_lab)
            all_products = Product.objects.filter(category__parent__parent=select_lab)
            work_type = Category.objects.filter(parent=select_lab)
            category = Category.objects.filter(parent__parent=select_lab)
            result = []
            for work in work_type:
                temp = []
                temp.append(work.name)
                work_type_category = Category.objects.filter(parent=work.id)
                temp.append(work_type_category)
                products = Product.objects.filter(category__parent__parent=select_lab)
                temp.append(products)
                result.append(temp)
            return render(request,'catalog/list_products.html',{'result':result,
                'root_name':root_name})


            # all_products = Product.objects.filter(category__parent__parent=select_lab)
            # all_categories=Category.objects.filter().order_by('name')
            # products_dict = { }
            # for one_category in all_categories:
            #     if one_category.is_leaf_node():
            #         one_category_dict = {}
            #         products_list = Product.objects.filter(category=one_category)
            #         attributes_dict = { }
            #         for one_product in products_list:
            #             attributes_list = Catalog.objects.filter(product = one_product)
            #             attributes_dict[one_product] = attributes_list
            #         one_category_dict[one_category.name] = attributes_dict
            #         products_dict[one_category.id] = one_category_dict
            # return render(request,'catalog/list_products.html',{'nodes':all_categories, \
            #     'products_dict':products_dict})
    else:
        form = ProductListForm()
        request_status = request_notify()
        return render(request,'catalog/product_list_form.html', \
        {'form':form,'request':request_status})


@login_required
def previous_value(request):
    """

    """
    old_post = request.session.get('old_post')
    purchase_order_id = request.session.get('purchase_order_id')
    Bill.objects.filter(purchase_order=purchase_order_id).delete()
    if SuspenseOrder.objects.filter(purchase_order=purchase_order_id):
        SuspenseOrder.objects.filter(purchase_order=purchase_order_id).delete()
    else:
        pass
    TaxesApplied.objects.\
    filter(purchase_order=purchase_order_id).delete()
    voucher_no = VoucherId.objects.values('voucher_no', 'session').\
    filter(purchase_order=purchase_order_id)
    for value in voucher_no:
        CalculateDistribution.objects.\
        get(voucher_no=value['voucher_no'], session=value['session']).delete()
    VoucherId.objects.filter(purchase_order=purchase_order_id).delete()
    return HttpResponseRedirect(reverse\
        ("voucher:voucher_generate"))

@login_required
def order_added_success(request):
    """
    This view displays Success message after order is successfully added
    Argument: Http Request
    Return: Render order_added_success.html
    """
    order_id = request.session.get('purchase_order_id')
    details = VoucherId.objects.values('purchase_order__buyer__first_name',\
        'purchase_order__buyer__last_name',
        'purchase_order__buyer__customer__address__street_address',\
        'purchase_order__buyer__customer__title',
        'purchase_order__buyer__customer__address__district',\
        'purchase_order__mode_of_payment__method',
        'purchase_order__cheque_dd_number',\
        'purchase_order__cheque_dd_date',
        'receipt_no_of_session').filter(purchase_order=order_id)[0]
    suspense_flag = 0
    suspense = SuspenseOrder.objects.filter(purchase_order=order_id)
    if suspense:
        suspense_flag = 1
    request_status = request_notify()
    return render(request,'catalog/order_added_success.html',\
        {'details': details,'order_id':order_id,'request':request_status,\
        'suspense_flag':suspense_flag})


@login_required
def change_request(request):
    """
    This view enables the user to add a change request or view a change request put by him
    Argument: Http Request
    Return: Render change_form.html
    """
    if request.method == 'POST':
        sessiondata = ChangeRequestForm(request.POST)
        purchase_order_of_session = sessiondata.data['purchase_order']
        session = sessiondata.data['session']
        object = VoucherId.objects.filter(session_id = session).\
        filter(purchase_order_of_session = purchase_order_of_session).values()
        if object:
            voucherid = VoucherId.objects.\
            filter(purchase_order_of_session=purchase_order_of_session,\
            session_id=session).values('purchase_order_id')
            for value in voucherid:
                purchase_order = value['purchase_order_id']
            bill = Bill.objects.values('grand_total').\
            get(purchase_order=purchase_order)
            surcharge = TaxesApplied.objects.values('surcharge__tax_name',\
                'id','tax').filter(purchase_order_id = purchase_order)
            details = VoucherId.objects.values\
            ('purchase_order__buyer__first_name',\
                'purchase_order__buyer__last_name',
                'purchase_order__buyer__customer__address__street_address',\
                'purchase_order__buyer__customer__title',
                'purchase_order__buyer__customer__address__district',\
                'purchase_order__mode_of_payment__method',
                'purchase_order__cheque_dd_number',\
                'purchase_order__cheque_dd_date').\
                filter(purchase_order_of_session=purchase_order_of_session)[0]
            session_data = FinancialSession.objects.values(\
                'session_start_date','session_end_date').get(id=session)
            messages = "Order" + " : " + purchase_order_of_session +\
            " and Session" + " : " + str(session_data['session_start_date']) +\
            ":" + str(session_data['session_end_date'])
            request_status = request_notify()    
            return render(request,'catalog/change_form.html',\
                {'details': details,'order_id':purchase_order_of_session,\
                'session':session,'surcharge':surcharge,'bill':bill,\
                'messages':messages, 'request':request_status})
        else:
                form = ChangeRequestForm()
                errors = "No such purchase order number in selected session" 
                request_status = request_notify()
                temp = {"form" : form , "errors" : errors,\
                'request':request_status}
                
                return render(request, 'catalog/change_request.html', temp) 
    else:
        form = ChangeRequestForm()
        request_status = request_notify()
        return render(request, 'catalog/change_request.html', \
            {'form':form,'request':request_status})


@login_required
def price_per_unit(request):
    """
    This view displays the price of a single unit of a product
    Argument: Http Request
    Return: Price Per Unit
    """
    item_id = request.GET['item_id']
    product = Product.objects.values('price_per_unit').get(id=item_id)
    if product['price_per_unit'] is not None:
        return HttpResponse(product['price_per_unit'])
    else:
        return HttpResponse('fail')


@login_required
def nonpaymentorderofsession(request):
    """
    This view enables the user to add a non payment order
    Argument: Http Request
    Return: Redirect to nonpaymentordersuccess view
    """
    old_post = request.session.get('old_post')
    nonpaymentorder_id = request.session.get('nonpaymentorder_id')
    try:
        nonpayobject = NonPaymentOrderOfSession.objects.values(
            'non_payment_order_of_session').\
        get(non_payment_order=nonpaymentorder_id)
        non_pay_order_id = nonpayobject['non_payment_order_of_session']
    except:
        non_pay_order = NonPaymentOrder.objects.values('date', 'id').\
        get(id=nonpaymentorder_id)
        nonpaymentorderobj=NonPaymentOrder.objects.get(id=nonpaymentorder_id)
        financialsession = FinancialSession.objects.\
        values('id','session_start_date','session_end_date')
        for value in financialsession:
            start_date = value['session_start_date']
            end_date = value['session_end_date']
            if start_date <= non_pay_order['date'] <= end_date:
                session_id = value['id']
        session = FinancialSession.objects.get(id = session_id)
        max_id = NonPaymentOrderOfSession.objects.all().aggregate(Max('id'))
        non_pay_order_id = 0
        if max_id['id__max'] == None:
            non_pay_order_id = 1
            obj = NonPaymentOrderOfSession(non_payment_order=nonpaymentorderobj,
                non_payment_order_of_session=1, session=session)
            obj.save()
        else:
            nonpayobj= NonPaymentOrderOfSession.objects.values(
                'non_payment_order_of_session', 'session').get(id = max_id['id__max'])
            if nonpayobj['session'] == session_id:
                non_pay_order_id = nonpayobj['non_payment_order_of_session'] + 1
                obj = NonPaymentOrderOfSession(non_payment_order=nonpaymentorderobj,
                    non_payment_order_of_session=non_pay_order_id,
                    session=session)
                obj.save()
            else:
                non_pay_order_id = 1
                obj = NonPaymentOrderOfSession(non_payment_order=nonpaymentorderobj,
                    non_payment_order_of_session=1, session=session)
                obj.save()
    request.session['old_post'] = old_post
    request.session['nonpaymentorder_id'] = nonpaymentorder_id
    return HttpResponseRedirect(\
        reverse("catalog:nonpaymentordersuccess"))


@login_required
def nonpaymentordersuccess(request):
    """
    This view displays success if a non payment order is added successfully
    Argument: Http Request
    Return: Render nonpaymentsuccess.html
    """
    old_post = request.session.get('old_post')
    nonpaymentorder_id = request.session.get('nonpaymentorder_id')
    details = NonPaymentOrder.objects.values('buyer__first_name',
        'buyer__last_name','buyer__customer__address__street_address',
        'buyer__customer__title','buyer__customer__address__district').\
    filter(id=nonpaymentorder_id)[0]
    nonpayobject = NonPaymentOrderOfSession.objects.values(
            'non_payment_order_of_session').\
    get(non_payment_order=nonpaymentorder_id)
    non_pay_order_id = nonpayobject['non_payment_order_of_session']
    return render(request, 'catalog/nonpaymentsuccess.html', {'data':old_post,
        'details':details, 'order_id':non_pay_order_id})
